from datetime import datetime
from sqlalchemy.orm import Session
from . import models
from .models import TxStatus

def get_rate(db: Session, code: str) -> float:
    """Возвращает последний курс валюты к BYN."""
    if code.upper() == "BYN":
        return 1.0
    
    rate_obj = db.query(models.ExchangeRate)\
        .filter(models.ExchangeRate.currency_code == code.upper())\
        .order_by(models.ExchangeRate.date.desc())\
        .first()
    
    if not rate_obj:
        raise ValueError(f"Нет курса для {code}")
    return float(rate_obj.rate)

def create_preview(db: Session, amount: float, from_code: str, to_code: str):
    # Считаем кросс-курс через BYN
    r_from = get_rate(db, from_code)
    r_to = get_rate(db, to_code)
    
    amount_to = round((amount * r_from) / r_to, 2)
    cross_rate = round(r_from / r_to, 4)
    
    tx = models.Transaction(
        status=TxStatus.pending,
        amount_from=amount,
        currency_from=from_code.upper(),
        amount_to=amount_to,
        currency_to=to_code.upper(),
        rate=cross_rate
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def confirm(db: Session, tx_id: int, action: str):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not tx:
        raise ValueError("Сделка не найдена")
    if tx.status != TxStatus.pending:
        raise ValueError("Сделка уже закрыта")
    
    if action == "confirm":
        tx.status = TxStatus.completed
    elif action == "reject":
        tx.status = TxStatus.rejected
    else:
        raise ValueError("Неверное действие")
        
    db.commit()
    return tx

def get_report(db: Session, start: datetime, end: datetime, curr: str = None):
    query = db.query(models.Transaction).filter(
        models.Transaction.status == TxStatus.completed,
        models.Transaction.created_at >= start,
        models.Transaction.created_at <= end
    )
    if curr:
        query = query.filter(
            (models.Transaction.currency_from == curr.upper()) | 
            (models.Transaction.currency_to == curr.upper())
        )
    
    txs = query.all()
    
    # Группируем результаты в питоне (в реальном проекте лучше делать SQL GROUP BY)
    result = {}
    for tx in txs:
        f = tx.currency_from
        t = tx.currency_to
        
        if f not in result:
            result[f] = {"received": 0, "given": 0, "count": 0}
        result[f]["received"] += float(tx.amount_from)
        result[f]["count"] += 1
        
        if t not in result:
            result[t] = {"received": 0, "given": 0, "count": 0}
        result[t]["given"] += float(tx.amount_to)
        result[t]["count"] += 1
    
    return [{"currency": k, "total_received": v["received"], "total_given": v["given"], "deals_count": v["count"]} for k, v in result.items()]

def get_pending(db: Session):
    return db.query(models.Transaction).filter(models.Transaction.status == TxStatus.pending).all()