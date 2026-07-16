import logging
from datetime import date, datetime, timedelta

from postgrest.exceptions import APIError

from app.core.exceptions import DataSourceUnavailable
from app.core.supabase_client import supabase

logger = logging.getLogger(__name__)

DAY_NAMES = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

ORDER = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]


class AnalyticsService:

    @staticmethod
    def get_weekly_sales(start_date: date, end_date: date):

        start_value = start_date.isoformat()

        # Se suma un día porque payment_date es TIMESTAMP.
        # Se utiliza un rango [inicio, fin)
        end_value = (
            end_date + timedelta(days=1)
        ).isoformat()

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
                .lt("payment_date", end_value)
                .execute()
            )

        except APIError:
            logger.exception(
                "weekly_sales_report_supabase_api_error"
            )
            raise DataSourceUnavailable()

        except Exception:
            logger.exception(
                "weekly_sales_report_unexpected_error"
            )
            raise

        sales_by_day = {}

        for payment in response.data:

            payment_date = payment.get("payment_date")

            amount = float(
                payment.get("amount") or 0
            )

            payment_datetime = datetime.fromisoformat(
                payment_date.replace(
                    "Z",
                    "+00:00"
                )
            )

            day = DAY_NAMES[
                payment_datetime.strftime("%A")
            ]

            sales_by_day[day] = (
                sales_by_day.get(day, 0)
                + amount
            )

        total_sales = sum(
            sales_by_day.values()
        )

        operations = len(
            response.data
        )

        average_ticket = (
            total_sales / operations
            if operations
            else 0
        )
        
        top_movies_response = (
            supabase.rpc(
                "top_movies_by_week",
                    {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                    },
            )
            .execute()
        )

        top_movies = top_movies_response.data

        total_rentals = sum(movie["rentals"] for movie in top_movies)

        # Ordenar los días de la semana
        sales_by_day = {
            day: sales_by_day[day]
            for day in ORDER
            if day in sales_by_day
        }

        logger.info(
            "weekly_sales_report_completed start_date=%s end_date=%s operations=%s total_sales=%.2f",
            start_value,
            end_date.isoformat(),
            operations,
            total_sales,
        )

        return {
            "start_date": start_value,
            "end_date": end_date.isoformat(),
            "total_sales": total_sales,
            "operations": operations,
            "average_ticket": average_ticket,
            "total_rentals": total_rentals,
            "sales_by_day": sales_by_day,
            "top_movies": top_movies,
        }