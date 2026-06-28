import logging
from datetime import date, datetime

from postgrest.exceptions import APIError

from app.core.exceptions import DataSourceUnavailable
from app.core.supabase_client import supabase

logger = logging.getLogger(__name__)


class AnalyticsService:

    @staticmethod
    def get_weekly_sales(start_date: date, end_date: date):
        start_value = start_date.isoformat()
        end_value = end_date.isoformat()

        logger.info(
            "weekly_sales_report_started start_date=%s end_date=%s",
            start_value,
            end_value,
        )

        try:
            response = (
                supabase
                .table("payment")
                .select("payment_date, amount")
                .gte("payment_date", start_value)
                .lte("payment_date", end_value)
                .execute()
            )
        except APIError:
            logger.exception("weekly_sales_report_supabase_api_error")
            raise DataSourceUnavailable()
        except Exception:
            logger.exception("weekly_sales_report_unexpected_error")
            raise

        sales_by_day = {
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0
        }

        for payment in response.data:
            payment_date = payment.get("payment_date")
            amount = payment.get("amount") or 0

            date = datetime.fromisoformat(
                payment_date.replace("Z", "+00:00")
            )

            day = date.strftime("%A")

            sales_by_day[day] += float(amount)

        total_sales = sum(sales_by_day.values())
        operations = len(response.data)

        logger.info(
            "weekly_sales_report_completed start_date=%s end_date=%s operations=%s total_sales=%.2f",
            start_value,
            end_value,
            operations,
            total_sales,
        )

        return {
            "start_date": start_value,
            "end_date": end_value,
            "total_sales": total_sales,
            "operations": operations,
            "average_ticket": total_sales / operations if operations else 0,
            "sales_by_day": sales_by_day
        }
