from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/exchange", tags=["Exchange"])

@router.post("/preview", response_model=schemas.ExchangePreview)
def preview(payload: schemas.ExchangeReq, db: Session = Depends(get_db)):
    try:
        tx = crud.create_preview(db, payload.amount, payload.currency_from, payload.currency_to)
        return tx
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/confirm", response_model=schemas.ConfirmResp)
def confirm(payload: schemas.ConfirmReq, db: Session = Depends(get_db)):
    try:
        tx = crud.confirm(db, payload.transaction_id, payload.action)
        return tx
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/report", response_model=schemas.ReportResp)
def report(
    start: datetime = Query(..., description="Начало периода"),
    end: datetime = Query(..., description="Конец периода"),
    currency: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    items = crud.get_report(db, start, end, currency)
    return {"items": items}

@router.get("/pending", response_model=list[schemas.PendingDeal])
def pending(db: Session = Depends(get_db)):
    return crud.get_pending(db)