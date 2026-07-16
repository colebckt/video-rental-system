from pydantic import BaseModel


class TopMovie(BaseModel):
    title: str
    rentals: int


class KPIResponse(BaseModel):
    start_date: str
    end_date: str
    total_sales: float
    operations: int
    average_ticket: float
    total_rentals: int
    sales_by_day: dict[str, float]
    top_movies: list[TopMovie]