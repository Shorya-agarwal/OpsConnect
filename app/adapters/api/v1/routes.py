import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.models import LeadPayload
from app.infra.dependencies import get_ingest_service, get_db_session
from app.core.use_cases.ingest import IngestService

router = APIRouter()

@router.post("/webhook", status_code=status.HTTP_201_CREATED)
async def ingest_salesforce_data(
    payload: LeadPayload,
    service: IngestService = Depends(get_ingest_service)
):
    """
    Receives data from Salesforce, validates it, and pushes to DB.
    Idempotent: Duplicate IDs are safely ignored.
    """
    result = await service.process_lead(payload)
    return result

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Checks DB connectivity and reports latency.
    Required by: DevOps / Kubernetes Liveness Probes.
    """
    start_time = time.time()
    try:
        # Simple query to check DB connection
        await db.execute(text("SELECT 1"))
        latency = (time.time() - start_time) * 1000 # to ms
        return {
            "status": "healthy",
            "db_latency_ms": round(latency, 2),
            "version": "0.1.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "reason": str(e)
        }, 503