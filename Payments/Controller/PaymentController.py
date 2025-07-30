import asyncio
from fastapi import APIRouter, status, Query

from Payments.Schema.CreateTransactionSchema import CreateTransaction
from Payments.Schema.SendTransaction import SendTransaction

from Payments.Service.Queue import *
from Payments.Service.Database import get_summary, filter_summary_by_datetime

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
async def get_payments_summary(date_from: datetime = Query(default=datetime.now(timezone.utc), alias="from"), date_to: datetime = Query(default=datetime.now(timezone.utc), alias="to")):
    transactions = await get_summary()
    
    return filter_summary_by_datetime(transactions, date_from, date_to)
