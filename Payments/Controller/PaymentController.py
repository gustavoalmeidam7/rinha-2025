import asyncio
from fastapi import APIRouter, status, Query

from Schema.CreateTransactionSchema import CreateTransaction
from Schema.SendTransaction import SendTransaction

from Service.Queue import *
from Service.Database import get_summary, filter_summary_by_datetime, convert_to_summary_schema

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
    transactions = filter_summary_by_datetime(transactions, date_from, date_to)
    
    return convert_to_summary_schema(transactions)
