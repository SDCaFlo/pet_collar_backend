from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from broker_api.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/health', tags=['health'])


@router.get("")
def health():
    return {"status": "ok"}


@router.get("/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok", "database": "ok"}
