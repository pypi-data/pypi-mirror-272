from fastapi import FastAPI
from .routers import trends
from .routers import items

def create_app():
    app = FastAPI(
        title="FashionTrendServer",
        description="APIs for FashionTrend",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc"
    )
    app.include_router(trends.router, tags=['trends'])
    app.include_router(items.router, tags=['items'])

    return app
