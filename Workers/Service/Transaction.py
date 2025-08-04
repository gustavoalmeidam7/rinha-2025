import asyncio
from httpx import AsyncClient

from Service.Queue import pop_transaction

from Schema.RequestResponse import RequestResponse
from Schema.SendTransaction import SendTransaction
from Schema.PaymentsSummaryScheme import Transaction

from Service.HealthService import healthStatuses, processors
from Service.Queue import insert_transaction

from Service.Database import append_values

from Utils.Env import env

WORKERS = env.get("workers")

async def retry_payment():
    transaction = await pop_transaction()

    if transaction is None:
        return

    paymentResult = await process_payment(transaction)

    transaction = Transaction.model_validate(transaction.model_dump())

    if paymentResult == RequestResponse.OK_FALLBACK or paymentResult == RequestResponse.OK_DEFAULT:
        isFallback = (True if paymentResult == RequestResponse.OK_FALLBACK else False)

        await append_values(transaction, isFallback)

async def run_workers():
    """
        Run the workers:
        Workers will get a payload from
        the redis queue and try to process them
    """
    if not env.get("run_workers"):
        print("Workers deactivated")
        return

    executeWorkersDelay = env.get("workers_insert_delay")

    while True:
        print("Running workers")
        for i in range(WORKERS):
            asyncio.create_task(retry_payment())

        await asyncio.sleep(executeWorkersDelay)

async def process_payment(transaction: SendTransaction) -> RequestResponse:
    """
        Try to process the payment:

        - RequestResponse.OK if the payment is processed successfulfy.
        - RequestResponse.INVALID_REQUEST if the payload is a invalid.
        - RequestResponse.UNAVALIBLE_PAYMENT_PROCESSOR if the payment
        processor is failing (Aka offline) or with a high latency the 
        payload is stored in a redis queue to be processed later.
    """
    if (not healthStatuses.Default.isFailing) and healthStatuses.Default.minResponseTime < 100:
        response = await do_request(transaction, processors.Default)
        
        if response == RequestResponse.OK_DEFAULT or response == RequestResponse.INVALID_REQUEST:
            return response
        
        await insert_transaction(transaction)
        return response

    elif (not healthStatuses.Fallback.isFailing) and healthStatuses.Fallback.minResponseTime < 100:
        response =  await do_request(transaction, processors.Fallback)

        if response == RequestResponse.OK_FALLBACK or response == RequestResponse.INVALID_REQUEST:
            return response
        
        await insert_transaction(transaction)
        return response
        
    else:
        await insert_transaction(transaction)
        return RequestResponse.UNAVALIBLE_PAYMENT_PROCESSOR

async def do_request(transaction: SendTransaction, processor: processors) -> RequestResponse:
    """
        Do the request to payment processor backend:
        
        - RequestResponse.OK if the request was successful (HTTP 200).
        - RequestResponse.UNAVALIBLE_PAYMENT_PROCESSOR if the processor
        is unavailable (HTTP 500).
        - RequestResponse.INVALID_REQUEST for other non-200 responses.
        - RequestResponse.TIME_OUT if an exception occurs during the
        request.
    """

    okResponse = RequestResponse.OK_FALLBACK if processor == processors.Fallback else RequestResponse.OK_DEFAULT

    async with AsyncClient() as client:
        try:
            print(transaction.model_dump())
            response = await client.post(url=processor.value + "/payments", json=transaction.model_dump())
                
            if response.status_code == 500:
                return RequestResponse.UNAVALIBLE_PAYMENT_PROCESSOR

            elif response.status_code != 200:
                print(response.text)
                return RequestResponse.INVALID_REQUEST

            else:
                return okResponse
        except Exception as e:
            print(e)
            return RequestResponse.TIME_OUT
