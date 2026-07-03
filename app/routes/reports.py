from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Query

from app.services.analytics_service import AnalyticsService
from app.models.report_models import KPIResponse


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# Reporte de ventas por semana
@router.get("/sales-report", response_model=KPIResponse)
def weekly_sales(
    start_date: date = Query(..., description="La fecha de inicio en formato YYYY-MM-DD"),
    end_date: date = Query(..., description="La fecha de fin en formato YYYY-MM-DD")
):
    if start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="La fecha de inicio debe ser menor o igual a la fecha de fin",
        )

    if end_date - start_date > timedelta(days=6):
        raise HTTPException(
            status_code=422,
            detail="El reporte de ventas semanales acepta un rango máximo de 7 días",
        )

    return AnalyticsService.get_weekly_sales(
        start_date,
        end_date
    )
