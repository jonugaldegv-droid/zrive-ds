from fastapi import FastAPI
from src.handlers import status, homepage, metrics
from src.metrics_middleware import MetricsMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title = 'Zrive DS - test API',
        version = '0.1.0'
    )

    app.add_middleware(MetricsMiddleware)

    app.include_router(homepage.router)
    app.include_router(status.router)
    app.include_router(metrics.router)

    return app
