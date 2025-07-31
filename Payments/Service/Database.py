from typing import List
from Payments.DB import redis

from Payments.Schema.PaymentsSummaryScheme import Transaction, PaymentsSummary

from datetime import datetime

async def append_values(transaction: Transaction, isFallback: bool):
    summary = await get_summary()

    transaction.isFallback = isFallback

    summary.Transactions.append(transaction)
    
    await update_summary(summary)
    return summary

async def update_summary(Transactions: PaymentsSummary):
    await redis.set("summary", str(Transactions.model_dump_json()))
    print(str(await redis.get("summary")))

def filter_summary_by_datetime(payments: PaymentsSummary, from_datetime: datetime, to_datetime: datetime) -> List[Transaction]:
    filtered_transactions = payments.Transactions
    filtered_transactions = filter(lambda d: d.requestedAt > from_datetime, filtered_transactions)
    filtered_transactions = filter(lambda d: d.requestedAt < to_datetime, filtered_transactions)

    return list(filtered_transactions)

async def get_summary() -> PaymentsSummary:
    summary = await redis.get("summary")
    if summary is None:
        return PaymentsSummary()
    
    return PaymentsSummary.model_validate_json(str(summary))
