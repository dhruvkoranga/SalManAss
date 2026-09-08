from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import EmployeeNotFoundError, InvalidCurrencyError
from app.routers.analytics import router as analytics_router
from app.routers.employees import router as employees_router

app = FastAPI(title="SalManAss")
app.include_router(employees_router)
app.include_router(analytics_router)


@app.exception_handler(EmployeeNotFoundError)
def handle_employee_not_found(request: Request, exc: EmployeeNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidCurrencyError)
def handle_invalid_currency(request: Request, exc: InvalidCurrencyError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
