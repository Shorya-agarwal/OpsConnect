from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.adapters.db.sessions import get_db_session
from app.adapters.db.repository import PostgresDBAdapter
from app.adapters.redis_adapter import RedisAdapter
from app.core.use_cases.ingest import IngestService

# Singleton Redis connection
# We don't want to open a new connection for every request
_redis_client = None

async def get_redis_adapter():
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisAdapter(settings.REDIS_URL)
    return _redis_client

# The Factory Function
# This assembles the "Use Case" by injecting the Adapters
def get_ingest_service(
    db: AsyncSession = Depends(get_db_session),
    cache: RedisAdapter = Depends(get_redis_adapter)
) -> IngestService:
    
    # 1. Initialize Adapters
    db_adapter = PostgresDBAdapter(db)
    
    # 2. Inject into Core Logic
    service = IngestService(db=db_adapter, cache=cache)
    
    return service