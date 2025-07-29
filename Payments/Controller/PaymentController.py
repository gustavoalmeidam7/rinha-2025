import asyncio
from fastapi import APIRouter, status, Query

from Payments.Schema.CreateTransactionSchema import CreateTransaction
from Payments.Schema.SendTransaction import SendTransaction
from Payments.Service.Queue import *

from datetime import datetime, timezone

PAYMENT_ROUTER = APIRouter(
    prefix="/payments",
    tags=[
        "Payments"
    ]
)

@PAYMENT_ROUTER.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(_transaction: CreateTransaction):
    transaction = SendTransaction.model_validate(_transaction.model_dump())
    
    await insert_transaction(transaction)

    return {"Body": "Ok"}

@PAYMENT_ROUTER.get("/payments-summary")
async def get_payments_summary(date_from: datetime = Query(default=datetime.now(timezone.utc), alias="from"), to: datetime = Query(default=datetime.now(timezone.utc), alias="to")):
    pass
