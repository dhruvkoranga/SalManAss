from decimal import Decimal

from pydantic import BaseModel, Field


class EmployeeUpdate(BaseModel):
    department: str
    job_title: str
    salary_amount: Decimal = Field(gt=0)
    currency_id: int
