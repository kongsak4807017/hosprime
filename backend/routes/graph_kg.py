import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.ai import chat_completion
from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, now_iso

router = APIRouter(prefix="/graph", tags=["knowledge-graph"])

NODE_TYPES = {
    "patient": {"label": "ผู้ป่วย", "color": "#2E77D0"},
    "doctor": {"label": "แพทย์", "color": "#1E3F33"},
    "department": {"label": "แผนก", "color": "#4A6B5D"},
    "drug": {"label": "ยา", "color": "#CC5A3A"},
    "condition": {"label": "โรค/ภาวะ", "color": "#D34228"},
    "allergen": {"label": "สารก่อภูมิแพ้", "color": "#E5A732"},
    "labtest": {"label": "การตรวจแล็บ", "color": "#327A59"},
}

EDGE_LABELS = {
    "TREATED_BY": "รักษาโดย",
    "HAS_CONDITION": "ป่วยเป็น",
    "ALLERGIC_TO": "แพ้",
    "TAKES": "ใช้ยา",
    "PRESCRIBED": "สั่งจ่าย",
    "BELONGS_TO": "สังกัด",
    "TESTED_WITH": "ตรวจ",
    "INTERACTS_WITH": "ตีกัน",
}

# Curated drug-drug interaction knowledge base (matched against drug names)
DRUG_INTERACTIONS = [
    ("Simvastatin", "Amlodipine", "เพิ่มความเสี่ยงกล้ามเนื้ออักเสบ (myopathy) — จำกัด simvastatin ไม่เกิน 20 mg/วัน"),
    ("Aspirin", "Losartan", "NSAID/aspirin อาจลดประสิทธิภาพยาลดความดันและเพิ่มความเสี่ยงต่อไต"),
    ("Omeprazole", "Cetirizine", "อาจเพิ่มระดับยาในเลือดเล็กน้อย — เฝ้าระวังอาการง่วงซึม"),
]


class GraphQuery(BaseModel):
    question: str


def _node(key: str, ntype: str, label: str, ref_id: str = "", props: dict = None):
    return {"key": key, "type": ntype, "label": label, "ref_id": ref_id, "props": props or {}}


@router.post("/build")
async def build_graph(user: dict = Depends(require_roles("admin", "doctor"))):
    """Build the department-level knowledge graph from operational data."""
    nodes = {}
    edges = {}

    def add_node(key, ntype, label, ref_id="", props=None):
        if key not in nodes:
            nodes[key] = _node(key, ntype, label, ref_id, props)
        return key

    def add_edge(src, dst, etype):
        ekey = f"{src}|{etype}|{dst}"
        if ekey in edges:
            edges[ekey]["weight"] += 1
        else:
            edges[ekey] = {"key": ekey, "source": src, "target": dst, "type": etype, "label": EDGE_LABELS[etype], "weight": 1}

    # Departments & doctors
    doctors = await db.users.find({"role": "doctor", "is_active": True}, {"_id": 0}).to_list(200)
    for d in doctors:
        dk = add_node(f"doctor:{d['id']}", "doctor", d["full_name"], d["id"], {"specialization": d.get("specialization", "")})
        if d.get("department"):
            dept = add_node(f"dept:{d['department']}", "department", d["department"])
            add_edge(dk, dept, "BELONGS_TO")

    # Drugs + interactions
    drugs = await db.drugs.find({"is_active": True}, {"_id": 0}).to_list(500)
    drug_nodes = {}
    for dr in drugs:
        key = add_node(f"drug:{dr['id']}", "drug", dr["name"], dr["id"], {"category": dr.get("category", ""), "stock": dr.get("quantity_in_stock", 0)})
        drug_nodes[dr["name"].lower()] = key
    for a, b, desc in DRUG_INTERACTIONS:
        ka = next((k for n, k in drug_nodes.items() if n.startswith(a.lower())), None)
        kb = next((k for n, k in drug_nodes.items() if n.startswith(b.lower())), None)
        if ka and kb:
            add_edge(ka, kb, "INTERACTS_WITH")
            edges[f"{ka}|INTERACTS_WITH|{kb}"]["props"] = {"description": desc}

    def match_drug(name: str):
        low = name.lower().strip()
        if not low:
            return None
        for n, k in drug_nodes.items():
            if n.startswith(low) or low in n:
                return k
        return add_node(f"drugname:{low}", "drug", name)

    # Patients
    patients = await db.patients.find({"is_active": True}, {"_id": 0}).to_list(2000)
    for p in patients:
        pk = add_node(f"patient:{p['id']}", "patient", f"{p['first_name']} {p['last_name']}", p["id"], {"patient_number": p["patient_number"], "blood_type": p.get("blood_type", "")})
        for c in p.get("chronic_conditions", []):
            if c.get("condition"):
                ck = add_node(f"condition:{c['condition']}", "condition", c["condition"])
                add_edge(pk, ck, "HAS_CONDITION")
        for a in p.get("allergies", []):
            if a.get("allergen"):
                ak = add_node(f"allergen:{a['allergen']}", "allergen", a["allergen"], props={"severity": a.get("severity", "")})
                add_edge(pk, ak, "ALLERGIC_TO")
        for m in p.get("current_medications", []):
            dk = match_drug(m.get("drug_name", ""))
            if dk:
                add_edge(pk, dk, "TAKES")

    # Appointments -> TREATED_BY
    appointments = await db.appointments.find({}, {"_id": 0, "patient_id": 1, "doctor_id": 1}).to_list(5000)
    for a in appointments:
        pk, dk = f"patient:{a['patient_id']}", f"doctor:{a['doctor_id']}"
        if pk in nodes and dk in nodes:
            add_edge(pk, dk, "TREATED_BY")

    # Prescriptions -> TAKES / PRESCRIBED
    prescriptions = await db.prescriptions.find({"status": {"$ne": "cancelled"}}, {"_id": 0}).to_list(5000)
    for pres in prescriptions:
        pk, dk = f"patient:{pres['patient_id']}", f"doctor:{pres['doctor_id']}"
        for med in pres.get("medications", []):
            mk = f"drug:{med['drug_id']}"
            if mk not in nodes:
                mk = match_drug(med.get("drug_name", ""))
            if mk:
                if pk in nodes:
                    add_edge(pk, mk, "TAKES")
                if dk in nodes:
                    add_edge(dk, mk, "PRESCRIBED")

    # Lab tests -> TESTED_WITH
    lab_tests = await db.lab_tests.find({"status": {"$ne": "cancelled"}}, {"_id": 0, "patient_id": 1, "test_type": 1}).to_list(5000)
    for t in lab_tests:
        pk = f"patient:{t['patient_id']}"
        lk = add_node(f"labtest:{t['test_type']}", "labtest", t["test_type"])
        if pk in nodes:
            add_edge(pk, lk, "TESTED_WITH")

    # Persist
    await db.kg_nodes.delete_many({})
    await db.kg_edges.delete_many({})
    if nodes:
        await db.kg_nodes.insert_many([dict(n) for n in nodes.values()])
    if edges:
        await db.kg_edges.insert_many([dict(e) for e in edges.values()])
    await db.settings.update_one(
        {"_id": "kg_meta"},
        {"$set": {"built_at": now_iso(), "built_by": user["full_name"], "node_count": len(nodes), "edge_count": len(edges)}},
        upsert=True,
    )
    await audit_log(user, "build", "knowledge_graph", "kg", f"{len(nodes)} nodes, {len(edges)} edges")

    by_type = {}
    for n in nodes.values():
        by_type[n["type"]] = by_type.get(n["type"], 0) + 1
    return {"node_count": len(nodes), "edge_count": len(edges), "nodes_by_type": by_type, "built_at": now_iso()}


@router.get("")
async def get_graph(node_type: str = "", limit: int = 500, user: dict = Depends(require_roles(*STAFF_ROLES))):
    query = {"type": node_type} if node_type else {}
    nodes = await db.kg_nodes.find(query, {"_id": 0}).limit(limit).to_list(limit)
    node_keys = {n["key"] for n in nodes}
    edges = await db.kg_edges.find({}, {"_id": 0}).to_list(5000)
    if node_type:
        # include neighbors of filtered nodes
        related_edges = [e for e in edges if e["source"] in node_keys or e["target"] in node_keys]
        neighbor_keys = {e["source"] for e in related_edges} | {e["target"] for e in related_edges}
        extra = await db.kg_nodes.find({"key": {"$in": list(neighbor_keys - node_keys)}}, {"_id": 0}).to_list(limit)
        nodes += extra
        node_keys |= {n["key"] for n in extra}
        edges = related_edges
    else:
        edges = [e for e in edges if e["source"] in node_keys and e["target"] in node_keys]
    meta = await db.settings.find_one({"_id": "kg_meta"}, {"_id": 0})
    return {"nodes": nodes, "edges": edges, "meta": meta, "node_types": NODE_TYPES}


@router.get("/stats")
async def graph_stats(user: dict = Depends(require_roles(*STAFF_ROLES))):
    meta = await db.settings.find_one({"_id": "kg_meta"}, {"_id": 0})
    by_type = await db.kg_nodes.aggregate([{"$group": {"_id": "$type", "count": {"$sum": 1}}}]).to_list(20)
    by_edge = await db.kg_edges.aggregate([{"$group": {"_id": "$type", "count": {"$sum": 1}}}]).to_list(20)
    return {
        "meta": meta,
        "nodes_by_type": {i["_id"]: i["count"] for i in by_type},
        "edges_by_type": {i["_id"]: i["count"] for i in by_edge},
        "node_types": NODE_TYPES,
        "edge_labels": EDGE_LABELS,
    }


@router.get("/node/{node_key:path}/neighbors")
async def node_neighbors(node_key: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    node = await db.kg_nodes.find_one({"key": node_key}, {"_id": 0})
    if not node:
        raise HTTPException(status_code=404, detail="ไม่พบโหนด")
    edges = await db.kg_edges.find({"$or": [{"source": node_key}, {"target": node_key}]}, {"_id": 0}).to_list(500)
    neighbor_keys = {e["source"] for e in edges} | {e["target"] for e in edges}
    neighbor_keys.discard(node_key)
    neighbors = await db.kg_nodes.find({"key": {"$in": list(neighbor_keys)}}, {"_id": 0}).to_list(500)
    return {"node": node, "edges": edges, "neighbors": neighbors}


def _build_query_context(question: str, nodes: list, edges: list) -> str:
    node_map = {n["key"]: n for n in nodes}
    q = question.lower()
    seeds = []
    for n in nodes:
        words = [w for w in n["label"].lower().replace("(", " ").replace(")", " ").split() if len(w) >= 3]
        if any(w in q for w in words):
            seeds.append(n["key"])
        if len(seeds) >= 15:
            break
    lines = []
    if seeds:
        seed_set = set(seeds)
        for e in edges:
            if e["source"] in seed_set or e["target"] in seed_set:
                s, t = node_map.get(e["source"]), node_map.get(e["target"])
                if s and t:
                    extra = f" ({e['props']['description']})" if e.get("props", {}).get("description") else ""
                    lines.append(f"{s['label']} ({NODE_TYPES[s['type']]['label']}) --[{e['label']}]--> {t['label']} ({NODE_TYPES[t['type']]['label']}){extra}")
            if len(lines) >= 120:
                break
    if not lines:
        # fallback: provide a broad sample of the graph
        for e in edges[:100]:
            s, t = node_map.get(e["source"]), node_map.get(e["target"])
            if s and t:
                lines.append(f"{s['label']} --[{e['label']}]--> {t['label']}")
    return "\n".join(lines)


@router.post("/query")
async def query_graph(body: GraphQuery, user: dict = Depends(require_roles(*STAFF_ROLES))):
    nodes = await db.kg_nodes.find({}, {"_id": 0}).to_list(3000)
    if not nodes:
        raise HTTPException(status_code=400, detail="ยังไม่มี Knowledge Graph กรุณากดสร้างกราฟก่อน")
    edges = await db.kg_edges.find({}, {"_id": 0}).to_list(10000)
    context = _build_query_context(body.question, nodes, edges)
    system = (
        "คุณคือ AI ผู้เชี่ยวชาญ Knowledge Graph ทางการแพทย์ของโรงพยาบาล HosPRIME "
        "ตอบคำถามจากข้อมูลความสัมพันธ์ในกราฟที่ให้เท่านั้น ตอบภาษาไทย กระชับ ชัดเจน "
        "หากเป็นเรื่องยาตีกันหรือการแพ้ยา ให้เน้นย้ำความปลอดภัยผู้ป่วย "
        "หากข้อมูลในกราฟไม่เพียงพอ ให้บอกตรงๆ"
    )
    try:
        answer = await chat_completion(
            system, [],
            f"ความสัมพันธ์ในกราฟ:\n{context}\n\nคำถาม: {body.question}",
            session_id=f"graph-query-{user['id']}",
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI ตอบไม่สำเร็จ: {str(e)[:200]}")
    return {"question": body.question, "answer": answer, "context_edges": len(context.splitlines())}
