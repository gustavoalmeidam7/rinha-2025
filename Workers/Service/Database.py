from Workers.DB import redis

from Workers.Schema.PaymentsSummaryScheme import Transaction, PaymentsSummary

async def append_values(transaction: Transaction, isFallback: bool):
    summary = await get_summary()

    summary.Transactions.append(transaction)
    
    await update_summary(summary)
    return summary

async def update_summary(Transactions: PaymentsSummary):
    await redis.set("summary", str(Transactions.model_dump()))
    print(str(await redis.get("summary")))

async def get_summary() -> PaymentsSummary:
    summary = await redis.get("summary")
    if summary is None:
        return PaymentsSummary()
    
    try:
        return PaymentsSummary.model_validate(summary)
    except:
        print("deleted all")
        await redis.delete("summary")
        return PaymentsSummary()
