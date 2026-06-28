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
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date in YYYY-MM-DD format")
):
    if start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="start_date must be less than or equal to end_date",
        )

    if end_date - start_date > timedelta(days=6):
        raise HTTPException(
            status_code=422,
            detail="The weekly sales report accepts a maximum range of 7 days",
        )

    return AnalyticsService.get_weekly_sales(
        start_date,
        end_date
    )
