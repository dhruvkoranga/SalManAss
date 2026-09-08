from sqlalchemy import create_engine, event, func, or_, select
from sqlalchemy.orm import Session, sessionmaker

from app.exceptions import EmployeeNotFoundError, InvalidCurrencyError
from app.models import Currency, Employee
from app.schemas import EmployeeUpdate


def create_session_factory(database_url: str, **engine_kwargs):
    engine = create_engine(database_url, **engine_kwargs)

    if database_url.startswith("sqlite"):
        # SQLite does not enforce foreign key constraints unless told to on
        # every connection. Without this, an Employee could reference a
        # currency_id that doesn't exist in the Currency table.
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine, sessionmaker(bind=engine, autoflush=False, autocommit=False)


def update_employee_salary(session: Session, employee_id: int, update: EmployeeUpdate) -> Employee:
    employee = session.get(Employee, employee_id)
    if employee is None:
        raise EmployeeNotFoundError(f"No employee with id {employee_id}")

    currency = session.get(Currency, update.currency_id)
    if currency is None:
        raise InvalidCurrencyError(f"No currency with id {update.currency_id}")

    employee.department = update.department
    employee.job_title = update.job_title
    employee.salary_amount = update.salary_amount
    employee.currency_id = update.currency_id
    session.commit()
    return employee


def list_employees(
    session: Session,
    *,
    search: str | None = None,
    country: str | None = None,
    department: str | None = None,
    job_title: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Employee], int]:
    query = select(Employee)

    if search:
        pattern = f"%{search}%"
        # ilike (not like) so this stays correct if the DB ever moves to
        # Postgres, where LIKE is case-sensitive unlike SQLite's default.
        query = query.where(
            or_(
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.email.ilike(pattern),
            )
        )
    if country:
        query = query.where(Employee.country == country)
    if department:
        query = query.where(Employee.department == department)
    if job_title:
        query = query.where(Employee.job_title == job_title)

    total = session.scalar(select(func.count()).select_from(query.subquery()))

    # A stable ORDER BY is required for LIMIT/OFFSET to return consistent
    # pages — without one, row order (and therefore pagination) isn't
    # guaranteed to stay the same between queries.
    items = session.scalars(
        query.order_by(Employee.last_name, Employee.first_name, Employee.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return list(items), total
