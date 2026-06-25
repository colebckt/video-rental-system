from pydantic import BaseModel

class KPIResponse(BaseModel):
    total_sales: float
    operations: int
    customers: int
    average_ticket: float