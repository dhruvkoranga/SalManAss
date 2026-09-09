from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_employee, get_filter_options, list_employees, update_employee_salary
from app.deps import get_db
from app.schemas import EmployeeFilterOptions, EmployeeListResponse, EmployeeRead, EmployeeUpdate

router = APIRouter(prefix="/api/employees", tags=["employees"])

SortField = Literal["first_name", "last_name", "country", "job_title", "salary_amount", "hire_date"]


@router.get("", response_model=EmployeeListResponse)
def get_employees(
    search: str | None = None,
    country: str | None = None,
    department: str | None = None,
    role: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: SortField | None = None,
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    items, total = list_employees(
        db,
        search=search,
        country=country,
        department=department,
        job_title=role,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return EmployeeListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/filters", response_model=EmployeeFilterOptions)
def get_employee_filters(db: Session = Depends(get_db)):
    return get_filter_options(db)


# Must come after /filters: FastAPI matches routes in registration order, and
# a route registered first would swallow "/filters" as an {employee_id}: int
# (failing with a 422, since "filters" isn't a valid int).
@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee_route(employee_id: int, db: Session = Depends(get_db)):
    return get_employee(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeRead)
def put_employee(employee_id: int, update: EmployeeUpdate, db: Session = Depends(get_db)):
    return update_employee_salary(db, employee_id, update)
