import structlog
from app.core.domain.models import LeadPayload
from app.core.ports import DatabasePort, CachePort

logger = structlog.get_logger()

class IngestService:
    def __init__(self, db: DatabasePort, cache: CachePort):
        # We inject the dependencies. 
        # The service doesn't know "how" save_lead works, just that it exists.
        self.db = db
        self.cache = cache

    async def process_lead(self, payload: LeadPayload) -> dict:
        """
        Orchestrates the ingestion logic:
        1. Check Idempotency (Redis)
        2. Log Structure
        3. Save to DB (Postgres)
        """
        # 1. Idempotency Check (The "Senior" Trait)
        cache_key = f"lead_processed:{payload.lead_id}"
        if await self.cache.get(cache_key):
            await logger.warning("duplicate_lead_detected", lead_id=payload.lead_id)
            return {"status": "skipped", "reason": "duplicate"}

        # 2. Structural Logging
        await logger.info("ingesting_lead", 
                          lead_id=payload.lead_id, 
                          email=payload.email, 
                          source=payload.source)

        # 3. Save to Database
        saved_lead = await self.db.save_lead(payload)

        # 4. Set Cache to prevent future duplicates (Expire in 24 hours)
        await self.cache.set(cache_key, "true", expire=86400)

        return {"status": "success", "lead_id": saved_lead.lead_id}