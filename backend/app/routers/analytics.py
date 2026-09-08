from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_analytics_summary
from app.deps import get_db
from app.schemas import AnalyticsSummary

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(db: Session = Depends(get_db)):
    return get_analytics_summary(db)
