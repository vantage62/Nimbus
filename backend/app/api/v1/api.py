from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from starlette.requests import Request
from app.core.config import settings

api_router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    timestamp: datetime
    request_id: Optional[str] = None

@api_router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check(request: Request):
    return HealthResponse(
        status="ok",
        version="1.0.0",
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow(),
        request_id=getattr(request.state, "request_id", None)
    )

# Import module routers
from app.modules.auth.router import router as auth_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.products.router import router as products_router
from app.modules.categories.router import router as categories_router
from app.modules.suppliers.router import router as suppliers_router
from app.modules.inventory.router import router as inventory_router
from app.modules.sales.router import router as sales_router
from app.modules.forecasting.router import router as forecasting_router
from app.modules.analytics.router import router as analytics_router
from app.modules.business.router import router as business_router
from app.modules.notifications.router import router as notifications_router
from app.modules.settings.router import router as settings_router
from app.modules.chat.router import router as chat_router
from app.modules.voice.router import router as voice_router
from app.modules.upload.router import router as upload_router

api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(products_router)
api_router.include_router(categories_router)
api_router.include_router(suppliers_router)
api_router.include_router(inventory_router)
api_router.include_router(sales_router)
api_router.include_router(forecasting_router)
api_router.include_router(analytics_router)
api_router.include_router(business_router)
api_router.include_router(notifications_router)
api_router.include_router(settings_router)
api_router.include_router(chat_router)
api_router.include_router(voice_router)
api_router.include_router(upload_router)
