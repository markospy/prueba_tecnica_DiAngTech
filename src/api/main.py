import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from api.exception_handlers import register_repository_exception_handlers
from api.routers.comment_router import comment_router
from api.routers.post_router import post_router
from api.routers.user_router import user_router
from core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
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
