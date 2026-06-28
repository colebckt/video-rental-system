from pydantic import BaseModel


class SalesByDay(BaseModel):
    Monday: float
    Tuesday: float
    Wednesday: float
    Thursday: float
    Friday: float
    Saturday: float
    Sunday: float


class KPIResponse(BaseModel):
    start_date: str
    end_date: str
    total_sales: float
    operations: int
    average_ticket: float
    sales_by_day: SalesByDay
