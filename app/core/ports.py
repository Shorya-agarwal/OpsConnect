from abc import ABC, abstractmethod
from typing import Optional
from app.core.domain.models import LeadPayload

class DatabasePort(ABC):
    """
    Interface for Database interactions. 
    The Core doesn't care if it's Postgres, MySQL, or a Mock.
    """
    @abstractmethod
    async def save_lead(self, lead: LeadPayload) -> LeadPayload:
        pass

    @abstractmethod
    async def get_lead(self, lead_id: str) -> Optional[LeadPayload]:
        pass

class CachePort(ABC):
    """
    Interface for Redis/Caching.
    Used for Idempotency (preventing duplicate processing).
    """
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int = 60) -> None:
        pass