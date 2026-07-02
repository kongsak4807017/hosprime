import json
import logging
from sqlalchemy.orm import Session
from backend.app.db.models import EntityRelation, DocumentChunk
from backend.app.services.graph_db_service import GraphDBService
from backend.app.services.gemini_service import GeminiService
from backend.app.agents.agents import log_agent_activity, RetrievalAgent

logger = logging.getLogger(__name__)

class GraphRAGAgent:
    @staticmethod
    def answer_query_with_graph(db: Session, query: str) -> dict:
        """[Milestone 4] ค้นหาข้อมูลเครือข่ายความสัมพันธ์ใน SQLite และทำ Graph-Vector RAG เพื่อหาคำตอบเชิงสืบสวน"""
        logger.info(f"GraphRAGAgent processing RAG Query: {query}")
        
        # 1. ค้นหาคำสัมพันธ์ (Entities/Relationships) จากตาราง SQLite
        # ดึงความสัมพันธ์ทั้งหมด
        relations = db.query(EntityRelation).all()
        
        # กรองความสัมพันธ์ที่คาดว่าเกี่ยวข้องกับคำถามผู้ใช้ (คีย์เวิร์ดตรงกัน)
        query_words = query.lower()
        matched_relations = []
        related_nodes = set()
        
        for rel in relations:
            src = rel.source_node.lower()
            tgt = rel.target_node.lower()
            rel_type = rel.relation_type.lower()
            
            # ตรวจจับความเกี่ยวข้อง
            if src in query_words or tgt in query_words or rel_type in query_words:
                matched_relations.append(rel)
                related_nodes.add(rel.source_node)
                related_nodes.add(rel.target_node)
                
        # หากได้ความสัมพันธ์น้อยเกินไป ดึงตัวเด่นๆ มาจำลองโครงข่ายเพิ่มเติม
        if len(matched_relations) < 3:
            matched_relations = relations[:6]
            for rel in matched_relations:
                related_nodes.add(rel.source_node)
                related_nodes.add(rel.target_node)

        # 2. ค้นหาชิ้นส่วนข้อความ (Vector Chunks) ด้วย RetrievalAgent
        vector_chunks = RetrievalAgent.retrieve(db, query, top_k=3)
        context_str = ""
        for idx, (chunk, score) in enumerate(vector_chunks):
            context_str += f"[Source {idx+1}]: {chunk.chunk_text}\n"

        # 3. จัดสร้าง Graph Context
        relations_str = ""
        nodes_list = []
        links_list = []
        
        for idx, rel in enumerate(matched_relations):
            relations_str += f"- ({rel.source_node}) -[{rel.relation_type}]-> ({rel.target_node})\n"
            
        # สร้าง Nodes & Links สำหรับส่งไปพล็อต Graph Visualizer
        unique_nodes = list(related_nodes)
        nodes_list = [{"id": node, "type": "Entity"} for node in unique_nodes]
        links_list = [
            {
                "source": rel.source_node, 
                "target": rel.target_node, 
                "type": rel.relation_type
            } for rel in matched_relations
        ]

        # 4. เรียกใช้ Gemini RAG ตอบคำถามโดยอ้างอิงข้อมูลท่อเชื่อมโยงความสัมพันธ์และข้อความ Vector
        system_instruction = (
            "You are the HosPrime Graph RAG Agent. "
            "You possess knowledge of both document text passages AND the relational Knowledge Graph of the organization. "
            "Synthesize an answer using both the provided relations and document sources. "
            "Be precise and show how entities (Roles, Departments, Programs) are connected."
        )
        
        prompt = (
            f"Query: {query}\n\n"
            f"--- KNOWLEDGE GRAPH RELATIONSHIPS ---\n"
            f"{relations_str}\n"
            f"--- DOCUMENT SOURCE PASSAGES ---\n"
            f"{context_str}\n\n"
            f"Please answer the query by reasoning through the graph and document context in Thai."
        )
        
        answer = GeminiService.generate_response(prompt, system_instruction)
        
        # 5. จัดส่งผลลัพธ์
        result = {
            "answer": answer,
            "confidence": 0.85,
            "subgraph": {
                "nodes": nodes_list,
                "links": links_list
            }
        }
        
        log_agent_activity(db, "GraphRAGAgent", "graph_rag", {"query": query}, {"answer": answer[:200]})
        return result
