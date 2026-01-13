import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.metrics_class import metrics

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            metrics.increase_exceptions()
            raise
        
        finally:
            metrics.increase_requests()

            elapsed = time.perf_counter() - start
            metrics.observe_latency(elapsed)

        return response