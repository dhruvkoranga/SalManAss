from datetime import date, datetime, timezone

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    symbol: Mapped[str] = mapped_column(String(5))
    # Value of 1 unit of this currency, expressed in INR. INR itself is 1.0.
    exchange_rate_to_inr: Mapped[float] = mapped_column(Numeric(12, 6))


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    country: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(100))
    job_title: Mapped[str] = mapped_column(String(100))
    salary_amount: Mapped[float] = mapped_column(Numeric(14, 2))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))
    hire_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=_utcnow, onupdate=_utcnow)

    currency: Mapped["Currency"] = relationship()
