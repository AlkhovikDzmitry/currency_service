from typing import List, Optional
from pydantic import BaseModel
from .models import TxStatus

class ExchangeReq(BaseModel):
    amount: float
    currency_from: str
    currency_to: str

class ExchangePreview(BaseModel):
    id: int
    amount_from: float
    currency_from: str
    amount_to: float
    currency_to: str
    rate: float

class ConfirmReq(BaseModel):
    transaction_id: int
    action: str 

class ConfirmResp(BaseModel):
    id: int
    status: TxStatus

class ReportRow(BaseModel):
    currency: str
    total_received: float
    total_given: float
    deals_count: int

class ReportResp(BaseModel):
    items: List[ReportRow]

class PendingDeal(BaseModel):
    id: int
    amount_from: float
    currency_from: str
    amount_to: float
    currency_to: str
    rate: float

    class Config:
        from_attributes = True