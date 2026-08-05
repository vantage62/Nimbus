from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.exceptions.base import NimbusException
from app.middleware.request_id import RequestLoggingMiddleware
from app.core.config import settings
from sqlalchemy.orm.exc import StaleDataError

app = FastAPI(
    title="Nimbus API",
    description="Nimbus SaaS platform backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# Global Exception Handler
@app.exception_handler(NimbusException)
async def nimbus_exception_handler(request: Request, exc: NimbusException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error", "code": "INTERNAL_ERROR"},
    )

@app.exception_handler(StaleDataError)
async def stale_data_exception_handler(request: Request, exc: StaleDataError):
    return JSONResponse(
        status_code=409,
        content={"success": False, "message": "Concurrent update conflict. Please refresh and try again.", "code": "CONFLICT"},
    )

# Include API Router
app.include_router(api_router, prefix="/api/v1")
