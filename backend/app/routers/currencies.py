from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import list_currencies
from app.deps import get_db
from app.schemas import CurrencyRead

router = APIRouter(prefix="/api/currencies", tags=["currencies"])


@router.get("", response_model=list[CurrencyRead])
def get_currencies(db: Session = Depends(get_db)):
    return list_currencies(db)
