import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.exception_handlers import register_repository_exception_handlers
from src.api.routers.comment_router import comment_router
from src.api.routers.post_router import post_router
from src.api.routers.register_login import app_security
from src.api.routers.tag_router import tag_router
from src.api.routers.user_router import user_router
from src.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(
    title="Prueba técnica de DiAngTech",
    description="API de prueba para la prueba técnica de DiAngTech",
    version="0.1.0",
    contact={"name": "Marcos Antonio Avila Morales", "email": "marcosantonioavilamorales@gmail.com"},
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    lifespan=lifespan,
)

register_repository_exception_handlers(app)

# CORS Configuration
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
    "max_age": 600,
}

app.add_middleware(CORSMiddleware, **CORS_CONFIG)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"route duration: {process_time:.3f} seconds")
    return response


app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(tag_router)
app.include_router(app_security)
