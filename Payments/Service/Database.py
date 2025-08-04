from typing import List
from DB import redis

from Schema.PaymentsSummaryScheme import Transaction, PaymentsSummary
from Schema.SummarySchema import SummarySchema

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
    filteredTransactions = payments.Transactions
    filteredTransactions = filter(lambda d: d.requestedAt > from_datetime, filteredTransactions)
    filteredTransactions = filter(lambda d: d.requestedAt < to_datetime, filteredTransactions)

    return list(filteredTransactions)

def convert_to_summary_schema(payments: list[Transaction]):
    summarySchema = SummarySchema()

    def do_processing_stuff(payment: Transaction):
        if payment.isFallback:
            summarySchema.fallback.totalAmount = payment.amount
            summarySchema.fallback.totalRequests += 1
            return
        
        summarySchema.default.totalAmount = payment.amount
        summarySchema.default.totalRequests += 1
        
    map(do_processing_stuff, payments)

    return summarySchema

async def get_summary() -> PaymentsSummary:
    summary = await redis.get("summary")
    if summary is None:
        return PaymentsSummary()
    
    return PaymentsSummary.model_validate_json(str(summary))
