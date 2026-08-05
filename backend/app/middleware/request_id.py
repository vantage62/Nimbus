import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            execution_time = time.time() - start_time
            
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "endpoint": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "execution_time": execution_time,
                    "timestamp": start_time
                }
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "endpoint": request.url.path,
                    "method": request.method,
                    "status_code": 500,
                    "execution_time": execution_time,
                    "timestamp": start_time,
                    "error": str(e)
                }
            )
            raise
