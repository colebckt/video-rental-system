from collections import defaultdict
from datetime import datetime
from app.core.supabase_client import supabase

class AnalyticsService:

    @staticmethod
    def get_weekly_sales(start_date: str, end_date: str):

        response = (
            supabase
            .table("payment")
            .select("payment_date, amount")
            .gte("payment_date", start_date)
            .lte("payment_date", end_date)
            .execute()
        )

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

            date = datetime.fromisoformat(
                payment["payment_date"]
            )

            day = date.strftime("%A")

            sales_by_day[day] += payment["amount"]

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_sales": sum(sales_by_day.values()),
            "operations": len(response.data),
            "average_ticket": sum(sales_by_day.values()) / len(response.data) if response.data else 0,
            "sales_by_day": sales_by_day
        }