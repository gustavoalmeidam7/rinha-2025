from DB import redis

from Schema.PaymentsSummaryScheme import Transaction, PaymentsSummary

async def append_values(transaction: Transaction, isFallback: bool):
    summary = await get_summary()

    transaction.isFallback = isFallback

    summary.Transactions.append(transaction)
    
    await update_summary(summary)
    return summary

async def update_summary(Transactions: PaymentsSummary):
    await redis.set("summary", str(Transactions.model_dump_json()))
    print(str(await redis.get("summary")))

async def get_summary() -> PaymentsSummary:
    summary = await redis.get("summary")
    if summary is None:
        return PaymentsSummary()
    
    return PaymentsSummary.model_validate_json(str(summary))
