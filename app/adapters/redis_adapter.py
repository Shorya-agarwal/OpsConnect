from typing import Optional
import redis.asyncio as redis
from app.core.ports import CachePort

class RedisAdapter(CachePort):
    def __init__(self, redis_url: str):
        # We use the async redis client
        self.client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: int = 60) -> None:
        await self.client.set(key, value, ex=expire)
    
    async def close(self):
        await self.client.close()