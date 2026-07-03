from pydantic import BaseModel


class KPIResponse(BaseModel):
    start_date: str
    end_date: str
    total_sales: float
    operations: int
    average_ticket: float
    sales_by_day: dict[str, float]