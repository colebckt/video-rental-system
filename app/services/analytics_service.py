import logging
from datetime import date, datetime, timedelta

from postgrest.exceptions import APIError

from app.core.exceptions import DataSourceUnavailable
from app.core.supabase_client import supabase

logger = logging.getLogger(__name__)


class AnalyticsService:

    @staticmethod
    def get_weekly_sales(start_date: date, end_date: date):

        start_value = start_date.isoformat()

        # Se suma un día porque payment_date es TIMESTAMP
        # y se utiliza un rango [inicio, fin)
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

        # Diccionario dinámico
        sales_by_day = {}
        
        # Diccionario para traducir los nombres de los días al español
        DAY_NAMES = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }

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
                (payment_datetime.strftime("%A"))
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

        logger.info(
            "weekly_sales_report_completed start_date=%s end_date=%s operations=%s total_sales=%.2f",
            start_value,
            end_value,
            operations,
            total_sales,
        )

        return {

            "start_date": start_value,

            # Se devuelve la fecha que ingresó el usuario,
            # no la utilizada internamente para el filtro.
            "end_date": end_date.isoformat(),

            "total_sales": total_sales,

            "operations": operations,

            "average_ticket": average_ticket,

            "sales_by_day": sales_by_day

        }