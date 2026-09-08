from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeUpdate(BaseModel):
    department: str
    job_title: str
    salary_amount: Decimal = Field(gt=0)
    currency_id: int


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str
    country: str
    department: str
    job_title: str
    salary_amount: Decimal
    currency_id: int
    hire_date: date


class EmployeeListResponse(BaseModel):
    items: list[EmployeeRead]
    total: int
    page: int
    page_size: int


class GroupStat(BaseModel):
    group: str
    average_salary_inr: Decimal
    median_salary_inr: Decimal
    count: int


class SalaryDistribution(BaseModel):
    minimum: Decimal
    p25: Decimal
    median: Decimal
    p75: Decimal
    maximum: Decimal


class AnalyticsSummary(BaseModel):
    by_country: list[GroupStat]
    by_department: list[GroupStat]
    by_role: list[GroupStat]
    salary_distribution: SalaryDistribution
