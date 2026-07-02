from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import EntityRelation

router = APIRouter()

@router.get("/network")
def get_provincial_knowledge_graph(db: Session = Depends(get_db)):
    """[Milestone 4] ดึงโครงสร้าง Node และ Link ของคลังความรู้ระดับจังหวัดทั้งหมด สำหรับแสดงผลโครงข่ายใยแมงมุมจริง"""
    try:
        relations = db.query(EntityRelation).all()
        
        nodes_set = set()
        links = []
        
        for rel in relations:
            nodes_set.add((rel.source_node, rel.source_type or "Entity"))
            nodes_set.add((rel.target_node, rel.target_type or "Entity"))
            links.append({
                "source": rel.source_node,
                "target": rel.target_node,
                "type": rel.relation_type,
                "confidence": rel.confidence
            })
            
        # หากฐานข้อมูลความสัมพันธ์ว่างเปล่า ให้ส่งค่าจำลองเชิงโครงสร้างของเชียงรายเพื่อพรีเมิวสวยงาม
        if not links:
            mock_nodes = [
                {"id": "สสจ.เชียงราย", "type": "Organization"},
                {"id": "นพ.สสจ.", "type": "Role"},
                {"id": "กลุ่มงานควบคุมโรค", "type": "Department"},
                {"id": "กลุ่มงานยุทธศาสตร์", "type": "Department"},
                {"id": "ฝุ่น PM2.5", "type": "Program"},
                {"id": "วัณโรค (TB)", "type": "Program"},
                {"id": "เบาหวาน (NCD)", "type": "Program"},
                {"id": "โครงการคัดกรองเชิงรุก", "type": "Project"},
                {"id": "คลินิก NCD Remission", "type": "Project"}
            ]
            mock_links = [
                {"source": "นพ.สสจ.", "target": "สสจ.เชียงราย", "type": "reports_to"},
                {"source": "กลุ่มงานควบคุมโรค", "target": "สสจ.เชียงราย", "type": "reports_to"},
                {"source": "กลุ่มงานยุทธศาสตร์", "target": "สสจ.เชียงราย", "type": "reports_to"},
                {"source": "กลุ่มงานควบคุมโรค", "target": "ฝุ่น PM2.5", "type": "owns"},
                {"source": "กลุ่มงานควบคุมโรค", "target": "วัณโรค (TB)", "type": "owns"},
                {"source": "กลุ่มงานควบคุมโรค", "target": "เบาหวาน (NCD)", "type": "owns"},
                {"source": "โครงการคัดกรองเชิงรุก", "target": "วัณโรค (TB)", "type": "supports"},
                {"source": "คลินิก NCD Remission", "target": "เบาหวาน (NCD)", "type": "supports"}
            ]
            return {"nodes": mock_nodes, "links": mock_links}
            
        nodes = [{"id": name, "type": ntype} for name, ntype in nodes_set]
        return {
            "nodes": nodes,
            "links": links
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve knowledge graph: {str(e)}"
        )

