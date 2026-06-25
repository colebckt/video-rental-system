from fastapi import APIRouter
import supabase
from app.services.analytics_service import AnalyticsService
from app.models.report_models import KPIResponse


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# Reporte de ventas por semana
@router.get("/sales-report")
def weekly_sales(
    start_date: str,
    end_date: str
):
    return AnalyticsService.get_weekly_sales(
        start_date,
        end_date
    )