from app.tasks.celery_app import celery_app
from app.services.ai_service import AIService
from app.schemas.ai import Message
from typing import List
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="ai.long_chat_completion")
def long_chat_completion(
    messages: List[dict],
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    org_id: int = None,
    user_id: int = None
) -> dict:
    """
    Background task for long-running AI requests
    
    Use this for requests that might take >10 seconds
    """
    try:
        # Convert dict to Message objects
        message_objects = [Message(**msg) for msg in messages]
        
        # Get AI response (sync version needed for Celery)
        import asyncio
        result = asyncio.run(
            AIService.chat_completion(
                messages=message_objects,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        )
        
        logger.info(f"Long AI request completed for org {org_id}")
        
        return {
            "status": "success",
            "result": result,
            "org_id": org_id,
            "user_id": user_id
        }
    
    except Exception as e:
        logger.error(f"Long AI request failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "org_id": org_id,
            "user_id": user_id
        }


@celery_app.task(name="ai.batch_process")
def batch_process_messages(
    messages_batch: List[dict],
    model: str,
    org_id: int
) -> dict:
    """
    Process multiple AI requests in batch
    
    Useful for bulk operations like:
    - Analyzing multiple documents
    - Generating multiple responses
    - Batch translations
    """
    results = []
    
    for item in messages_batch:
        try:
            messages = [Message(**msg) for msg in item["messages"]]
            
            import asyncio
            result = asyncio.run(
                AIService.chat_completion(
                    messages=messages,
                    model=model
                )
            )
            
            results.append({
                "id": item.get("id"),
                "status": "success",
                "result": result
            })
        
        except Exception as e:
            results.append({
                "id": item.get("id"),
                "status": "error",
                "error": str(e)
            })
    
    return {
        "org_id": org_id,
        "total": len(messages_batch),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "results": results
    }
