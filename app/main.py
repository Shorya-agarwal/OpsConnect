from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.settings import settings
from app.infra.logging_conf import configure_logging
from app.infra.telemetry import setup_telemetry
from app.adapters.api.v1.routes import router as v1_router
import uvicorn
# Lifecycle event to handle startup/shutdown logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Configure Logs
    configure_logging(json_logs=(settings.ENV != "dev"))
    yield
    # Shutdown: (Cleanup logic if needed)

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

# Setup Tracing
if settings.ENV != "dev":
   setup_telemetry(app)

# Include Routes
app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)