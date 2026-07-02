import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.db.models import QueryLog
from backend.app.schemas.schemas import QueryRequest, QueryResponse, FeedbackRequest, QueryLogResponse
from backend.app.agents.agents import (
    RetrievalAgent, RerankingAgent, AnswerGenerationAgent, CitationAgent, FeedbackLearningAgent
)

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
def ask_oracle(request: QueryRequest, db: Session = Depends(get_db)):
    """ถามคำถาม RAG จากคลังความรู้องค์กร"""
    query = request.question.strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty")
        
    try:
        # 1. ค้นหาชิ้นส่วนความรู้ที่ใกล้เคียง (Top 8)
        retrieved = RetrievalAgent.retrieve(db, query, top_k=8)
        
        # 2. จัดเรียง/คัดเลือกชิ้นส่วนที่ดีที่สุดใหม่ (Reranking)
        reranked = RerankingAgent.rerank(db, query, retrieved)
        
        # 3. นำชิ้นส่วนที่ดีที่สุด 5 อันดับแรกมาสร้างคำตอบ (Grounded QA)
        answer, confidence = AnswerGenerationAgent.generate_answer(db, query, reranked[:5])
        
        # 4. สร้างแผงข้อมูลการอ้างอิง (Citations)
        sources_info = CitationAgent.map_citations(answer, reranked[:5])
        
        # 5. บันทึกคำถามและคำตอบลงใน QueryLog
        # บันทึก sources ในรูป JSON
        sources_json = json.dumps([{
            "document_id": src["document_id"],
            "document_title": src["document_title"],
            "page_number": src["page_number"],
            "section_title": src["section_title"],
            "score": src["score"]
        } for src in sources_info], ensure_ascii=False)
        
        query_log = QueryLog(
            user_id=request.user_id,
            question=query,
            answer=answer,
            sources=sources_json,
            confidence=confidence
        )
        db.add(query_log)
        db.commit()
        db.refresh(query_log)
        
        return QueryResponse(
            answer=answer,
            sources=sources_info,
            confidence=confidence,
            query_log_id=query_log.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while querying the Knowledge Oracle: {str(e)}"
        )

@router.post("/logs/{log_id}/feedback")
def submit_feedback(log_id: int, request: FeedbackRequest, db: Session = Depends(get_db)):
    """ส่งฟีดแบคให้กับคำตอบ (Like/Dislike)"""
    success = FeedbackLearningAgent.record_feedback(db, log_id, request.feedback)
    if not success:
        raise HTTPException(status_code=404, detail="Query log not found")
    return {"message": "Feedback recorded successfully"}

@router.get("/logs", response_model=List[QueryLogResponse])
def get_query_logs(db: Session = Depends(get_db)):
    """ดึงประวัติการสอบถามและคำตอบล่าสุด"""
    logs = db.query(QueryLog).order_by(QueryLog.created_at.desc()).limit(100).all()
    
    response_logs = []
    for log in logs:
        sources_list = []
        if log.sources:
            try:
                sources_list = json.loads(log.sources)
            except Exception:
                pass
        
        response_logs.append(QueryLogResponse(
            id=log.id,
            user_id=log.user_id,
            question=log.question,
            answer=log.answer,
            sources=sources_list,
            confidence=log.confidence,
            feedback=log.feedback,
            created_at=log.created_at
        ))
    return response_logs
