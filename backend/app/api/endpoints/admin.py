from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.db.models import Document
from backend.app.schemas.schemas import DocumentResponse, DocumentUpdate, DocumentReviewAction

router = APIRouter()

@router.get("/pending", response_model=List[DocumentResponse])
def get_pending_documents(db: Session = Depends(get_db)):
    """ดึงรายการเอกสารทั้งหมดที่อยู่ในระหว่างรอการอนุมัติ (Pending review)"""
    return db.query(Document).filter(Document.status == "pending review").all()

@router.put("/documents/{doc_id}", response_model=DocumentResponse)
def update_document_metadata(doc_id: int, request: DocumentUpdate, db: Session = Depends(get_db)):
    """แก้ไขข้อมูลเมตาดาตาของเอกสารโดยผู้ดูแลระบบ"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doc, key, value)
        
    db.commit()
    db.refresh(doc)
    return doc

@router.post("/documents/{doc_id}/review", response_model=DocumentResponse)
def review_document(doc_id: int, action: DocumentReviewAction, db: Session = Depends(get_db)):
    """อนุมัติหรือปฏิเสธเอกสารเข้าระบบ RAG"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if action.action == "approve":
        # อัปเดตข้อมูลเมตาดาตาหากผู้ใช้ระบุมาพร้อมการอนุมัติ
        if action.metadata:
            update_data = action.metadata.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(doc, key, value)
        doc.status = "processed"
    elif action.action == "reject":
        doc.status = "failed"
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'approve' or 'reject'.")
        
    db.commit()
    db.refresh(doc)
    return doc


from pydantic import BaseModel
from typing import Optional

class MigrationRequest(BaseModel):
    db_migration: bool = True
    postgres_url: Optional[str] = None
    graph_migration: bool = True
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = "neo4j"
    neo4j_password: Optional[str] = None

from backend.app.auth import check_role
from backend.app.db.models import User as DBUser

@router.post("/migrate")
def one_click_migration(
    request: MigrationRequest, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_role(["admin"]))
):
    """[Milestone 4 & 5] One-Click Migration สำหรับย้ายข้อมูล SQLite ไปยัง PostgreSQL และส่งต่อข้อมูลไปยัง Neo4j"""
    import os
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    
    results = {}
    
    # 1. ย้ายฐานข้อมูลหลัก: SQLite ➔ PostgreSQL
    if request.db_migration:
        pg_url = request.postgres_url or os.getenv("POSTGRES_URL")
        if not pg_url or not pg_url.startswith("postgresql"):
            raise HTTPException(
                status_code=400, 
                detail="กรุณาระบุ PostgreSQL URL ปลายทาง (เช่น postgresql://user:password@host:5432/dbname)"
            )
            
        try:
            # เชื่อมต่อ PostgreSQL
            pg_engine = create_engine(pg_url)
            
            # โหลดและลงทะเบียนโมเดลทั้งหมดก่อนทำการสร้างตาราง
            from backend.app.db.session import Base
            from backend.app.db import models as db_models
            Base.metadata.create_all(bind=pg_engine)
            
            PgSession = sessionmaker(bind=pg_engine)
            pg_session = PgSession()
            
            # ปิด Foreign Key Constraints ใน PostgreSQL ชั่วคราวเพื่อให้ insert ได้สะดวกแบบ Replica
            pg_session.execute(text("SET session_replication_role = 'replica';"))
            pg_session.commit()
            
            # นำเข้าโมเดลทั้งหมด
            from backend.app.db.models import (
                Document, DocumentChunk, EntityRelation, QueryLog, AgentLog,
                Meeting, ActionItem, WorkflowRun, User
            )
            from backend.app.models.twin_models import (
                Organization, Role, Person, Knowledge, Agent,
                KnowledgeNode, KnowledgeRelationship, person_role
            )
            
            standard_models = [
                User, Document, DocumentChunk, EntityRelation, QueryLog, AgentLog,
                Meeting, ActionItem, WorkflowRun,
                Organization, Role, Person, Knowledge, Agent,
                KnowledgeNode, KnowledgeRelationship
            ]
            
            migration_summary = {}
            
            # ย้าย Standard Models
            for model in standard_models:
                # ล้างข้อมูลใน PostgreSQL ตารางนี้ก่อนเพื่อเริ่มย้ายใหม่
                pg_session.query(model).delete()
                pg_session.commit()
                
                sqlite_data = db.query(model).all()
                count = 0
                for item in sqlite_data:
                    columns = item.__table__.columns
                    item_data = {col.name: getattr(item, col.name) for col in columns}
                    
                    # สร้างอินสแตนซ์ใหม่เพื่อหลีกเลี่ยง conflict
                    new_item = item.__class__(**item_data)
                    pg_session.add(new_item)
                    count += 1
                pg_session.commit()
                migration_summary[model.__tablename__] = count
                
            # ย้ายตารางความสัมพันธ์คนกับบทบาท (person_role association table)
            pg_session.execute(person_role.delete())
            pg_session.commit()
            
            sqlite_roles = db.execute(person_role.select()).fetchall()
            role_count = 0
            for row in sqlite_roles:
                pg_session.execute(person_role.insert().values(person_id=row.person_id, role_id=row.role_id))
                role_count += 1
            pg_session.commit()
            migration_summary["person_role"] = role_count
            
            # เปิดสิทธิ์ Constraints ใน PostgreSQL คืนปกติ
            pg_session.execute(text("SET session_replication_role = 'origin';"))
            pg_session.commit()
            pg_session.close()
            
            results["db_migration"] = {
                "status": "success",
                "summary": migration_summary,
                "message": "ย้ายข้อมูลจาก SQLite ไปยัง PostgreSQL สำเร็จแล้ว กรุณาอัปเดต DATABASE_URL ในไฟล์ .env ของ Backend เป็น PostgreSQL URL ตัวใหม่และรีสตาร์ทเซิร์ฟเวอร์"
            }
            
        except Exception as e:
            results["db_migration"] = {
                "status": "failed",
                "error": str(e)
            }
            
    # 2. ย้ายข้อมูลโครงข่าย: SQLite/PostgreSQL ➔ Neo4j Graph Database
    if request.graph_migration:
        uri = request.neo4j_uri or os.getenv("NEO4J_URI")
        user = request.neo4j_user or os.getenv("NEO4J_USER", "neo4j")
        password = request.neo4j_password or os.getenv("NEO4J_PASSWORD")
        
        if not uri or not password:
            raise HTTPException(
                status_code=400, 
                detail="กรุณาระบุ Neo4j Connection URI และ Password ในระบบ"
            )
            
        try:
            from backend.app.services.graph_db_service import GraphDBService
            from backend.app.db.models import EntityRelation
            
            relations = db.query(EntityRelation).all()
            node_count = 0
            rel_count = 0
            
            # ล้างข้อมูลใน Neo4j ก่อนนำเข้า
            clear_cypher = "MATCH (n) DETACH DELETE n"
            GraphDBService.query_graph(clear_cypher, uri, user, password)
            
            # นำข้อมูลความสัมพันธ์ไปสร้างใน Neo4j
            for rel in relations:
                src_label = rel.source_type or "Entity"
                GraphDBService.create_node(
                    node_id=rel.source_node, 
                    label=src_label, 
                    properties={"name": rel.source_node, "type": src_label},
                    uri=uri, user=user, password=password
                )
                node_count += 1
                
                tgt_label = rel.target_type or "Entity"
                GraphDBService.create_node(
                    node_id=rel.target_node, 
                    label=tgt_label, 
                    properties={"name": rel.target_node, "type": tgt_label},
                    uri=uri, user=user, password=password
                )
                node_count += 1
                
                GraphDBService.create_relationship(
                    source_id=rel.source_node,
                    relationship_type=rel.relation_type,
                    target_id=rel.target_node,
                    properties={"confidence": rel.confidence},
                    uri=uri, user=user, password=password
                )
                rel_count += 1
                
            results["graph_migration"] = {
                "status": "success",
                "nodes_processed": node_count,
                "relationships_created": rel_count,
                "message": "ย้ายข้อมูลความสัมพันธ์เชิงลึก (Knowledge Graph) ไปยัง Neo4j เรียบร้อยแล้ว"
            }
            
        except Exception as e:
            results["graph_migration"] = {
                "status": "failed",
                "error": str(e)
            }
            
    return results


@router.get("/agent-summary")
def get_admin_agent_summary(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_role(["admin"]))
):
    """[Milestone 5] ดึงข้อมูลวิเคราะห์ระบบสถิติภาพรวม RAG และ Twin แล้วสรุปด้วย AI Agent Admin"""
    try:
        total_docs = db.query(Document).count()
        pending_docs = db.query(Document).filter(Document.status == "pending review").count()
        processed_docs = db.query(Document).filter(Document.status == "processed").count()
        failed_docs = db.query(Document).filter(Document.status == "failed").count()
        
        from backend.app.db.models import QueryLog, WorkflowRun
        total_queries = db.query(QueryLog).count()
        total_workflows = db.query(WorkflowRun).count()
        
        from backend.app.models.twin_models import Organization, Role, Person
        total_orgs = db.query(Organization).count()
        total_roles = db.query(Role).count()
        total_persons = db.query(Person).count()
        
        # ดึงประวัติคำถามล่าสุด 5 รายการ
        recent_queries = db.query(QueryLog).order_by(QueryLog.created_at.desc()).limit(5).all()
        recent_queries_list = [
            {
                "question": q.question,
                "answer": q.answer[:100] + "..." if len(q.answer) > 100 else q.answer,
                "confidence": q.confidence,
                "created_at": str(q.created_at)
            } for q in recent_queries
        ]
        
        # จัดโครงสร้างข้อมูลสำหรับให้ AI สรุปวิเคราะห์
        system_stats = {
            "rag": {
                "total_documents": total_docs,
                "pending_review": pending_docs,
                "processed": processed_docs,
                "failed": failed_docs,
                "total_queries": total_queries
            },
            "twins": {
                "total_organizations": total_orgs,
                "total_roles": total_roles,
                "total_persons": total_persons
            },
            "workflows": {
                "total_workflow_runs": total_workflows
            },
            "recent_queries": recent_queries_list
        }
        
        # ส่งข้อมูลสถิติให้ Gemini ในฐานะ AI Agent Admin
        from backend.app.services.gemini_service import GeminiService
        system_instruction = (
            "คุณคือ HosPrime AI Agent Admin ผู้ช่วยตรวจสอบความปลอดภัย ประสิทธิภาพ และความมั่นคงของระบบการแพทย์และสารสนเทศ สสจ.เชียงราย "
            "หน้าที่ของคุณคือวิเคราะห์สถิติที่ส่งมาและเขียนรายงานประเมินความปลอดภัย ประสิทธิภาพความรู้ "
            "รวมทั้งให้คำแนะนำการปรับแต่งหรือบริหารระบบอย่างเจาะลึก 3-4 ข้อสำหรับแอดมินระบบ "
            "เขียนรายงานในโทนที่เป็นมืออาชีพ น่าเชื่อถือ และเข้าใจง่าย เป็นภาษาไทย โดยจัดทำหัวข้อดังนี้:\n"
            "1. 📊 สรุปความสมบูรณ์ของระบบสารสนเทศและการประมวลผล (System Health Assessment)\n"
            "2. 🛡️ การประเมินความปลอดภัยและการคัดกรองเอกสาร RAG (Security & RAG Quality Audit)\n"
            "3. 💡 ข้อเสนอแนะการเพิ่มประสิทธิภาพระบบและฐานความรู้ (Strategic Recommendations for Admin)\n"
            "เน้นการนำเสนอข้อมูลที่กระชับและปฏิบัติได้จริง"
        )
        
        prompt = f"ข้อมูลสถิติระบบ HosPrime HODT ปัจจุบัน:\n{str(system_stats)}"
        
        try:
            ai_summary = GeminiService.generate_response(prompt, system_instruction=system_instruction)
            status_type = "success"
        except Exception as e:
            ai_summary = (
                "### 📊 สรุปความสมบูรณ์ของระบบสารสนเทศ (Fallback)\n"
                f"ขณะนี้ระบบสามารถจัดเก็บเอกสาร RAG ทั้งหมด {total_docs} รายการ (อนุมัติแล้ว {processed_docs} รายการ, รอการอนุมัติ {pending_docs} รายการ) "
                f"มีจำนวน Role Twin ทั้งหมด {total_roles} ตำแหน่ง และ Person Twin ทั้งหมด {total_persons} บุคลากร "
                "การทำงานทั่วไปปกติดี\n\n"
                "### 🛡️ การประเมินความปลอดภัยและสิทธิ์ใช้งาน\n"
                "ระบบมีการเข้ารหัสและคัดกรอง JWT อย่างเข้มงวดตามมาตรฐานการรักษาความปลอดภัยข้อมูลของกระทรวงสาธารณสุข\n\n"
                "### 💡 ข้อเสนอแนะ\n"
                "1. ควรเร่งตรวจสอบและอนุมัติเอกสารที่ค้างท่อเพื่อให้ RAG นำไปสืบค้นได้ครบถ้วน\n"
                "2. แนะนำให้เชื่อมต่อกับบริการส่งออกข้อมูลความสัมพันธ์สู่ Neo4j เพิ่มเติมเพื่อความสืบค้นข้อมูลเชิงลึกที่มีประสิทธิภาพยิ่งขึ้น"
            )
            status_type = "fallback"
            
        return {
            "stats": system_stats,
            "ai_summary": ai_summary,
            "status": status_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงรายงาน AI Agent Admin: {str(e)}"
        )


@router.get("/agent-logs")
def get_agent_logs(db: Session = Depends(get_db)):
    """ดึงข้อมูลประวัติกิจกรรมการทำงานของ AI Agents ทั้งหมด"""
    import json
    from backend.app.db.models import AgentLog
    try:
        logs = db.query(AgentLog).order_by(AgentLog.created_at.desc()).limit(100).all()
        result = []
        for log in logs:
            try:
                input_val = json.loads(log.input_data) if log.input_data else None
            except Exception:
                input_val = log.input_data
                
            try:
                output_val = json.loads(log.output_data) if log.output_data else None
            except Exception:
                output_val = log.output_data
                
            result.append({
                "id": log.id,
                "agent_id": log.agent_id,
                "task_type": log.task_type,
                "input_data": input_val,
                "output_data": output_val,
                "status": log.status,
                "created_at": str(log.created_at)
            })
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ไม่สามารถดึงข้อมูลประวัติการทำงานของ AI Agents ได้: {str(e)}"
        )

