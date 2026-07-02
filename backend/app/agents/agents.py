import json
import logging
import numpy as np
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.db.models import Document, DocumentChunk, EntityRelation, QueryLog, AgentLog
from backend.app.services.document_parser import DocumentParser
from backend.app.services.gemini_service import GeminiService
from backend.app.services.ai_gateway import AIGateway
from backend.app.services.graph_db_service import GraphDBService

logger = logging.getLogger(__name__)

# Helper function for logging agent operations
def log_agent_activity(db: Session, agent_id: str, task_type: str, input_data: Any, output_data: Any, status: str = "success"):
    try:
        agent_log = AgentLog(
            agent_id=agent_id,
            task_type=task_type,
            input_data=json.dumps(input_data, ensure_ascii=False) if isinstance(input_data, (dict, list)) else str(input_data),
            output_data=json.dumps(output_data, ensure_ascii=False) if isinstance(output_data, (dict, list)) else str(output_data),
            status=status
        )
        db.add(agent_log)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log agent activity: {e}")

class KnowledgeIngestionAgent:
    @staticmethod
    def ingest(db: Session, file_path: str, title: str, confidentiality_level: str = "Internal") -> Document:
        """นำเข้าเอกสาร สกัดข้อความดิบ จัดเก็บใน Database และเขียนเชื่อมสัมพันธ์ลง Neo4j"""
        logger.info(f"Ingesting document: {file_path}")
        
        # 1. สร้าง Document record เบื้องต้น
        doc = Document(
            title=title,
            file_path=file_path,
            confidentiality_level=confidentiality_level,
            status="processing"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        try:
            # 2. เรียกใช้ Parser เพื่อสกัดข้อความ
            pages_data = DocumentParser.parse_document(file_path)
            
            # บันทึกกิจกรรมของ Agent
            log_agent_activity(
                db, 
                agent_id="KnowledgeIngestionAgent", 
                task_type="text_extraction", 
                input_data={"file_path": file_path}, 
                output_data={"pages_count": len(pages_data), "status": "extracted"}
            )
            
            # 3. จัดประเภทเอกสารและสกัดเมตาดาตาเชิงลึก
            sample_text = "\n".join([page["text"] for page in pages_data[:2]])
            
            metadata = MetadataAgent.extract_metadata_and_relations(db, doc.id, sample_text)
            doc_type_info = DocumentClassificationAgent.classify(db, sample_text)
            
            # อัปเดตข้อมูลเมตาดาตาของเอกสาร
            doc.document_type = doc_type_info.get("document_type", "Report")
            doc.department = metadata.get("department", "Unknown")
            doc.program = metadata.get("program", "General")
            doc.year = metadata.get("year", "Unknown")
            doc.owner = metadata.get("owner", "Unknown")
            
            # 4. แบ่งชิ้นข้อมูล (Chunking)
            chunks = ChunkingAgent.chunk_document(pages_data)
            
            # 5. สร้าง Embeddings และจัดเก็บ Chunk
            EmbeddingAgent.embed_and_store(db, doc.id, chunks)
            
            # 6. บันทึกความสัมพันธ์ลงใน Neo4j Graph DB จริง (Enterprise Pipeline)
            try:
                relations = metadata.get("relations", [])
                for rel in relations:
                    # สร้าง Node แหล่งข้อมูลและผู้รับผิดชอบ
                    GraphDBService.create_node(
                        node_id=f"doc_{doc.id}",
                        label="Document",
                        properties={"title": title, "program": doc.program, "owner": doc.owner}
                    )
                    source_id = rel.get("source_node")
                    target_id = rel.get("target_node")
                    if source_id and target_id:
                        GraphDBService.create_node(node_id=source_id, label=rel.get("source_type", "Entity"))
                        GraphDBService.create_node(node_id=target_id, label=rel.get("target_type", "Entity"))
                        GraphDBService.create_relationship(
                            source_id=source_id,
                            relationship_type=rel.get("relation_type", "RELATED_TO").upper(),
                            target_id=target_id
                        )
            except Exception as graph_err:
                logger.error(f"Failed to index entities in Neo4j Graph DB: {graph_err}")
            
            doc.status = "processed"
            db.commit()
            
            log_agent_activity(
                db, 
                agent_id="KnowledgeIngestionAgent", 
                task_type="complete_ingestion", 
                input_data={"document_id": doc.id}, 
                output_data={"status": "success", "chunks_count": len(chunks)}
            )
            
        except Exception as e:
            logger.error(f"Failed to ingest document {file_path}: {e}")
            doc.status = "failed"
            db.commit()
            log_agent_activity(
                db, 
                agent_id="KnowledgeIngestionAgent", 
                task_type="complete_ingestion", 
                input_data={"document_id": doc.id}, 
                output_data={"status": "failed", "error": str(e)},
                status="failed"
            )
            raise e
            
        return doc

class DocumentClassificationAgent:
    @staticmethod
    def classify(db: Session, text_sample: str) -> Dict[str, Any]:
        """คัดแยกประเภทของเอกสารโดยใช้ LLM"""
        system_instruction = (
            "You are an expert Document Classification Agent in public health. "
            "Classify the document into one of the following types: Policy, SOP, Meeting Notes, Report. "
            "You must return ONLY a JSON object with keys: 'document_type' and 'confidence_score' (between 0.0 and 1.0)."
        )
        
        prompt = (
            f"Analyze this document sample and determine its category:\n\n"
            f"--- START DOCUMENT SAMPLE ---\n"
            f"{text_sample[:3000]}\n"
            f"--- END DOCUMENT SAMPLE ---"
        )
        
        result = AIGateway.generate_json_response(db, prompt, system_instruction, agent_id="DocumentClassificationAgent")
        
        if not result or "document_type" not in result:
            result = {"document_type": "Report", "confidence_score": 0.5}
            
        log_agent_activity(db, "DocumentClassificationAgent", "classification", prompt[:300], result)
        return result

class MetadataAgent:
    @staticmethod
    def extract_metadata_and_relations(db: Session, doc_id: int, text_sample: str) -> Dict[str, Any]:
        """สกัดเมตาดาตาอัตโนมัติและความสัมพันธ์ระดับ HODT"""
        system_instruction = (
            "You are a Public Health Digital Transformation Metadata Agent. "
            "Analyze the document text and extract metadata and key entities and their relationships. "
            "Return a JSON object with structure:\n"
            "{\n"
            "  'department': 'e.g. กลุ่มงานควบคุมโรค, กลุ่มงานยุทธศาสตร์',\n"
            "  'program': 'e.g. PM2.5, TB, NCD, Disaster, Digital Health (choose most relevant, default to General)',\n"
            "  'year': 'e.g. 2568 (Buddhist era year)',\n"
            "  'owner': 'e.g. นพ.สสจ.เชียงราย, นายแพทย์สาธารณสุขจังหวัด',\n"
            "  'relations': [\n"
            "     {'source_node': 'A', 'relation_type': 'owns/reports_to/affects/supports', 'target_node': 'B', 'source_type': 'Person/Role/Department', 'target_type': 'Role/Department/KPI/Project'}\n"
            "  ]\n"
            "}"
        )
        
        prompt = (
            f"Analyze this public health document and extract metadata and relations:\n\n"
            f"{text_sample[:4000]}"
        )
        
        result = AIGateway.generate_json_response(db, prompt, system_instruction, agent_id="MetadataAgent")
        
        relations = result.get("relations", [])
        for rel in relations:
            try:
                db_rel = EntityRelation(
                    document_id=doc_id,
                    source_node=rel.get("source_node"),
                    relation_type=rel.get("relation_type"),
                    target_node=rel.get("target_node"),
                    source_type=rel.get("source_type"),
                    target_type=rel.get("target_type"),
                    confidence=1.0
                )
                db.add(db_rel)
            except Exception as e:
                logger.warning(f"Failed to store entity relation: {e}")
        db.commit()
        
        log_agent_activity(db, "MetadataAgent", "metadata_extraction", prompt[:300], result)
        return result

class ChunkingAgent:
    @staticmethod
    def chunk_document(pages_data: List[Dict[str, Any]], chunk_size: int = 800, overlap: int = 150) -> List[Dict[str, Any]]:
        """แบ่งข้อความหน้าเอกสารออกเป็นท่อนย่อย (Chunks) เพื่อทำ Index"""
        chunks = []
        
        for page in pages_data:
            text = page["text"]
            page_num = page["page_number"]
            section_title = page["section_title"]
            
            if len(text) <= chunk_size:
                chunks.append({
                    "chunk_text": text,
                    "page_number": page_num,
                    "section_title": section_title
                })
                continue
                
            start = 0
            while start < len(text):
                end = start + chunk_size
                if end < len(text):
                    last_space = text.rfind("\n", start + chunk_size - 100, end)
                    if last_space != -1 and last_space > start:
                        end = last_space
                
                chunk_text = text[start:end].strip()
                if chunk_text:
                    chunks.append({
                        "chunk_text": chunk_text,
                        "page_number": page_num,
                        "section_title": section_title
                    })
                start += (chunk_size - overlap)
                
        return chunks

class EmbeddingAgent:
    @staticmethod
    def embed_and_store(db: Session, doc_id: int, chunks: List[Dict[str, Any]]):
        """คำนวณเวกเตอร์ Embedding และจัดเก็บบันทึกลงใน PostgreSQL / SQLite"""
        for idx, chunk in enumerate(chunks):
            text_content = chunk["chunk_text"]
            embedding = GeminiService.get_embedding(text_content)
            
            # บันทึกลงตาราง DocumentChunk โดยรองรับคอลัมน์ Vector
            db_chunk = DocumentChunk(
                document_id=doc_id,
                chunk_text=text_content,
                page_number=chunk["page_number"],
                section_title=chunk["section_title"],
                embedding_id=f"doc_{doc_id}_chunk_{idx}",
                token_count=len(text_content) // 4,
                embedding_data=json.dumps(embedding),
                embedding=embedding # เก็บลงฟิลด์ pgvector โดยตรง ( SQLAlchemy type SafeVector จะแปลงตาม Dialect)
            )
            db.add(db_chunk)
        db.commit()

class RetrievalAgent:
    @staticmethod
    def retrieve(db: Session, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """ค้นหาท่อนข้อมูลที่คล้ายกับคำค้นหาโดยใช้ pgvector (PostgreSQL) หรือ Fallback Cosine Scan (SQLite)"""
        # 1. แปลงคำถามผู้ใช้เป็นเวกเตอร์
        query_vector = GeminiService.get_embedding(query, is_query=True)
        
        # 2. ตรวจสอบ Dialect ของฐานข้อมูล
        dialect_name = db.bind.dialect.name
        
        if dialect_name == "postgresql":
            try:
                logger.info("Using PostgreSQL pgvector HNSW Index search pipeline.")
                # แปลงเวกเตอร์เป็นรูปแบบข้อความสำหรับ pgvector SQL string "[v1, v2, ...]"
                query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"
                
                # ค้นหาผ่าน SQL query ดิบ เพื่อหลีกเลี่ยงข้อจำกัดการนำเข้าไลบรารี pgvector ในโค้ด SQLite
                sql_query = text("""
                    SELECT dc.id, (1 - (dc.embedding <=> :vector::vector)) as similarity 
                    FROM document_chunks dc
                    JOIN documents d ON dc.document_id = d.id
                    WHERE d.status = 'processed'
                    ORDER BY dc.embedding <=> :vector::vector
                    LIMIT :limit
                """)
                
                raw_results = db.execute(sql_query, {"vector": query_vector_str, "limit": top_k}).fetchall()
                
                # แมปผลลัพธ์กลับไปยัง DocumentChunk object
                results = []
                for chunk_id, score in raw_results:
                    chunk = db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
                    if chunk:
                        results.append((chunk, float(score)))
                return results
                
            except Exception as pg_err:
                logger.error(f"PostgreSQL pgvector search failed: {pg_err}. Falling back to in-memory cosine scan.")
                
        # 3. Fallback: ดึง Chunks ทั้งหมดมาเปรียบเทียบในหน่วยความจำ Python ( SQLite Mode )
        query_np = np.array(query_vector)
        chunks = db.query(DocumentChunk).join(Document).filter(Document.status == "processed").all()
        
        results = []
        for chunk in chunks:
            vector = None
            if chunk.embedding is not None:
                vector = chunk.embedding
            elif chunk.embedding_data:
                try:
                    vector = json.loads(chunk.embedding_data)
                except Exception:
                    pass
            
            if not vector:
                continue
                
            chunk_np = np.array(vector)
            
            dot_product = np.dot(query_np, chunk_np)
            norm_q = np.linalg.norm(query_np)
            norm_c = np.linalg.norm(chunk_np)
            
            score = float(dot_product / (norm_q * norm_c)) if norm_q > 0 and norm_c > 0 else 0.0
            results.append((chunk, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

class RerankingAgent:
    @staticmethod
    def rerank(db: Session, query: str, retrieved_chunks: List[Tuple[DocumentChunk, float]]) -> List[Tuple[DocumentChunk, float]]:
        """จัดลำดับความสัมพันธ์ของข้อมูลเพิ่มเติม เช่น เพิ่มน้ำหนักถ้าเป็นแผนก/แฟ้มงานที่ตรงตรงกับคำถาม"""
        query_lower = query.lower()
        reranked = []
        
        for chunk, score in retrieved_chunks:
            weight = 1.0
            doc = chunk.document
            
            if doc.program and doc.program.lower() in query_lower:
                weight += 0.15
            if doc.department and doc.department.lower() in query_lower:
                weight += 0.1
                
            adjusted_score = min(score * weight, 1.0)
            reranked.append((chunk, adjusted_score))
            
        reranked.sort(key=lambda x: x[1], reverse=True)
        
        log_agent_activity(
            db, 
            "RerankingAgent", 
            "rerank", 
            {"query": query, "input_count": len(retrieved_chunks)}, 
            {"output_ids": [c[0].id for c in reranked]}
        )
        return reranked

class AnswerGenerationAgent:
    @staticmethod
    def generate_answer(db: Session, query: str, context_chunks: List[Tuple[DocumentChunk, float]]) -> Tuple[str, float]:
        """สังเคราะห์คำตอบจากเอกสารอ้างอิงทั้งหมด โดยใช้เงื่อนไขที่รัดกุมที่สุด"""
        if not context_chunks or context_chunks[0][1] < 0.25:
            return "Evidence is insufficient from the current organizational knowledge base.", 0.0

        context_str = ""
        for idx, (chunk, score) in enumerate(context_chunks):
            doc = chunk.document
            context_str += (
                f"[Source ID: {idx+1}]\n"
                f"Document: {doc.title} (Page {chunk.page_number or 'Unknown'}, Department: {doc.department or 'N/A'})\n"
                f"Content: {chunk.chunk_text}\n"
                f"Similarity Score: {score:.4f}\n\n"
            )
            
        system_instruction = (
            "You are the Health Organization Operating System (HosPrime) Knowledge Oracle. "
            "Your answer must be grounded ONLY on the provided document sources. "
            "Do not fabricate or use outside knowledge. If the provided sources do not contain information "
            "to answer the question, you MUST reply: 'Evidence is insufficient from the current organizational knowledge base.'\n\n"
            "Your output must follow this strict structure in THAI:\n"
            "# Executive Summary\n"
            "[Brief summary of the response]\n\n"
            "# Key Findings\n"
            "[List key findings from sources]\n\n"
            "# Evidence\n"
            "[Provide explicit facts and details cited with [Source ID: X] referencing page numbers if available]\n\n"
            "# Caution / Limitation\n"
            "[Mention gaps, limitations, weak data, or assumptions from the sources]\n\n"
            "# Recommended Next Step\n"
            "[Suggest next steps based strictly on recommendations in the sources]\n\n"
            "# Sources / Citations\n"
            "[List all cited source documents with their file path or title]"
        )

        prompt = (
            f"Question: {query}\n\n"
            f"--- START SOURCES ---\n"
            f"{context_str}\n"
            f"--- END SOURCES ---\n\n"
            f"Answer using the format specified."
        )

        confidence = float(np.mean([score for _, score in context_chunks]))
        
        # ค้นหาคำตอบโดยใช้ AI Gateway (ส่วน Swappable Brains)
        answer = AIGateway.generate_response(
            db=db,
            prompt=prompt,
            system_instruction=system_instruction,
            model_name="gemini-1.5-pro",
            temperature=0.2,
            agent_id="AnswerGenerationAgent"
        )
        
        log_agent_activity(db, "AnswerGenerationAgent", "generate_answer", {"query": query}, {"answer": answer[:200], "confidence": confidence})
        return answer, confidence

class CitationAgent:
    @staticmethod
    def map_citations(answer: str, context_chunks: List[Tuple[DocumentChunk, float]]) -> List[Dict[str, Any]]:
        """วิเคราะห์คำตอบและจัดรูปแบบแหล่งอ้างอิงส่งกลับไปฝั่ง Client"""
        citations = []
        for idx, (chunk, score) in enumerate(context_chunks):
            doc = chunk.document
            citations.append({
                "source_id": idx + 1,
                "document_id": doc.id,
                "document_title": doc.title,
                "chunk_id": chunk.id,
                "chunk_text": chunk.chunk_text,
                "page_number": chunk.page_number,
                "section_title": chunk.section_title,
                "score": score
            })
        return citations

class FeedbackLearningAgent:
    @staticmethod
    def record_feedback(db: Session, log_id: int, feedback_type: str) -> bool:
        """บันทึกข้อมูลตอบกลับการใช้งาน"""
        log = db.query(QueryLog).filter(QueryLog.id == log_id).first()
        if log:
            log.feedback = feedback_type
            db.commit()
            
            log_agent_activity(db, "FeedbackLearningAgent", "save_feedback", {"log_id": log_id, "feedback": feedback_type}, "recorded")
            return True
        return False
