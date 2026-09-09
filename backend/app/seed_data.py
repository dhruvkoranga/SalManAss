"""Synthetic employee data for the seed script (backend/scripts/seed.py).

Kept separate from the script itself so the generation logic can be unit
tested without touching a real database file.
"""

import random
from datetime import date, timedelta

from app.models import Employee

CURRENCIES = [
    {"code": "INR", "symbol": "₹", "exchange_rate_to_inr": 1},
    {"code": "USD", "symbol": "$", "exchange_rate_to_inr": 83},
    {"code": "GBP", "symbol": "£", "exchange_rate_to_inr": 105},
    {"code": "EUR", "symbol": "€", "exchange_rate_to_inr": 90},
    {"code": "SGD", "symbol": "S$", "exchange_rate_to_inr": 62},
    {"code": "AUD", "symbol": "A$", "exchange_rate_to_inr": 55},
]

COUNTRY_CURRENCY = {
    "India": "INR",
    "United States": "USD",
    "United Kingdom": "GBP",
    "Germany": "EUR",
    "Singapore": "SGD",
    "Australia": "AUD",
}

# (department, job_title, min_salary_inr, max_salary_inr) — bands are annual,
# INR-equivalent, so role level (not country) drives the analytics story.
ROLES = [
    ("Engineering", "Software Engineer", 800_000, 1_600_000),
    ("Engineering", "Engineering Manager", 1_800_000, 3_200_000),
    ("Sales", "Sales Executive", 500_000, 1_000_000),
    ("Sales", "Sales Manager", 1_500_000, 2_800_000),
    ("Marketing", "Marketing Specialist", 550_000, 1_100_000),
    ("Marketing", "Marketing Manager", 1_400_000, 2_600_000),
    ("Human Resources", "HR Executive", 450_000, 900_000),
    ("Human Resources", "HR Manager", 1_300_000, 2_400_000),
    ("Finance", "Financial Analyst", 600_000, 1_200_000),
    ("Finance", "Finance Manager", 1_600_000, 3_000_000),
    ("Operations", "Operations Executive", 500_000, 1_000_000),
    ("Operations", "Operations Manager", 1_400_000, 2_600_000),
    ("Product", "Product Manager", 1_500_000, 2_800_000),
    ("Product", "Senior Product Manager", 2_500_000, 4_200_000),
    ("Design", "Product Designer", 700_000, 1_400_000),
    ("Design", "Design Lead", 1_800_000, 3_200_000),
    ("Customer Support", "Support Specialist", 400_000, 800_000),
    ("Customer Support", "Support Manager", 1_200_000, 2_200_000),
    ("Legal", "Legal Counsel", 1_500_000, 3_000_000),
    ("Legal", "Compliance Officer", 1_200_000, 2_400_000),
]

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Ishaan", "Kabir", "Rohan", "Ananya", "Diya",
    "Priya", "Neha", "James", "John", "Robert", "Michael", "William", "David",
    "Mary", "Patricia", "Jennifer", "Linda", "Oliver", "George", "Harry",
    "Jack", "Charlotte", "Amelia", "Emily", "Sophie", "Lukas", "Felix",
    "Hannah", "Anna", "Wei", "Jian", "Mei", "Ling", "Liam", "Noah", "Emma",
    "Olivia",
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Iyer", "Nair", "Reddy", "Kapoor", "Mehta",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis",
    "Wilson", "Taylor", "Anderson", "Thomas", "Moore", "Mueller", "Schmidt",
    "Fischer", "Weber", "Wagner", "Becker", "Tan", "Lim", "Lee", "Wong",
    "Ng", "Chen", "Kumar", "Singh", "Patel", "Khan", "Clarke", "Evans",
    "Roberts", "Walker",
]

EARLIEST_HIRE_DATE = date(2018, 1, 1)
LATEST_HIRE_DATE = date(2026, 9, 9)

_RATE_BY_CURRENCY_CODE = {c["code"]: c["exchange_rate_to_inr"] for c in CURRENCIES}


def _random_hire_date(rng: random.Random) -> date:
    span_days = (LATEST_HIRE_DATE - EARLIEST_HIRE_DATE).days
    return EARLIEST_HIRE_DATE + timedelta(days=rng.randint(0, span_days))


def build_employees(
    n: int,
    currency_ids: dict[str, int],
    rng: random.Random | None = None,
) -> list[Employee]:
    """Generate n unpersisted Employee objects.

    currency_ids maps currency code (e.g. "USD") to the Currency row's
    primary key, so callers must insert the Currency rows first.
    """
    rng = rng or random.Random()
    countries = list(COUNTRY_CURRENCY)

    employees = []
    for i in range(n):
        country = rng.choice(countries)
        currency_code = COUNTRY_CURRENCY[country]
        exchange_rate = _RATE_BY_CURRENCY_CODE[currency_code]

        department, job_title, min_salary_inr, max_salary_inr = rng.choice(ROLES)
        salary_inr = rng.uniform(min_salary_inr, max_salary_inr)
        salary_amount = round(salary_inr / exchange_rate, 2)

        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        # Index suffix guarantees uniqueness even with a small name pool.
        email = f"{first_name.lower()}.{last_name.lower()}{i}@acme.example"

        employees.append(
            Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                country=country,
                department=department,
                job_title=job_title,
                salary_amount=salary_amount,
                currency_id=currency_ids[currency_code],
                hire_date=_random_hire_date(rng),
            )
        )

    return employees
