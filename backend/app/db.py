from sqlalchemy import create_engine, event
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
