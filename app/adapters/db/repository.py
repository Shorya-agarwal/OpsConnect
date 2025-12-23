from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.ports import DatabasePort
from app.core.domain.models import LeadPayload
from app.adapters.db.orm import LeadTable

class PostgresDBAdapter(DatabasePort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_lead(self, lead: LeadPayload) -> LeadPayload:
        # 1. Convert Domain Model (Pydantic) -> DB Model (ORM)
        lead_db = LeadTable(
            lead_id=lead.lead_id,
            email=lead.email,
            first_name=lead.first_name,
            last_name=lead.last_name,
            source=lead.source,
            signup_date=lead.signup_date,
            is_processed=True
        )

        # 2. Add to session and commit
        self.session.add(lead_db)
        await self.session.commit()
        await self.session.refresh(lead_db)

        # 3. Convert back: DB Model -> Domain Model
        return LeadPayload.model_validate(lead_db)

    async def get_lead(self, lead_id: str) -> Optional[LeadPayload]:
        query = select(LeadTable).where(LeadTable.lead_id == lead_id)
        result = await self.session.execute(query)
        lead_db = result.scalar_one_or_none()

        if lead_db:
            return LeadPayload.model_validate(lead_db)
        return None