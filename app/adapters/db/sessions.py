from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import settings

# 1. Create the Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENV == "dev"), # Log SQL queries in dev mode
    future=True
)

# 2. Create the Session Factory
# We use this to spawn a new DB session for every request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Dependency for FastAPI (We will use this in Step 4)
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session