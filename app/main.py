import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import AnalyticsError
from app.core.logging_config import configure_logging
from app.core.supabase_client import supabase
from app.routes.reports import router

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Analytics Service",
    version="1.0.0",
    description="Modulo 6 - Servicio independiente de reportes financieros Sakila."
)

app.include_router(router)


@app.middleware("http")
async def request_logger(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "request_failed request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )
        raise

    duration_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed request_id=%s method=%s path=%s status_code=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.exception_handler(AnalyticsError)
async def analytics_error_handler(request: Request, exc: AnalyticsError):
    logger.warning(
        "analytics_error path=%s status_code=%s message=%s",
        request.url.path,
        exc.status_code,
        exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "service": settings.service_name,
        },
    )


@app.get("/")
def root():
    return {
        "service": settings.service_name,
        "status": "running",
        "module": "Modulo 6 - Finanzas",
        "screen": "Reporte de ventas por semana"
    }
    

@app.get("/health")
def health_live():
    return {
        "status": "UP",
        "service": settings.service_name
    }


@app.get("/health/live")
def live():
    return {
        "status": "UP",
        "service": settings.service_name
    }


@app.get("/health/ready")
def ready():
    try:
        supabase.table("payment").select("payment_id").limit(1).execute()
    except Exception:
        logger.exception("readiness_check_failed")
        return JSONResponse(
            status_code=503,
            content={
                "status": "DOWN",
                "service": settings.service_name,
                "dependency": "supabase",
            },
        )

    return {
        "status": "UP",
        "service": settings.service_name,
        "dependency": "supabase"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)
