import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions import EmployeeNotFoundError, InvalidCurrencyError
from app.routers.analytics import router as analytics_router
from app.routers.currencies import router as currencies_router
from app.routers.employees import router as employees_router

app = FastAPI(title="SalManAss")

# Render deploys the frontend and backend as separate services (different
# origins), so CORS is required in production, not just local dev.
allowed_origins = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees_router)
app.include_router(analytics_router)
app.include_router(currencies_router)


@app.exception_handler(EmployeeNotFoundError)
def handle_employee_not_found(request: Request, exc: EmployeeNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidCurrencyError)
def handle_invalid_currency(request: Request, exc: InvalidCurrencyError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
