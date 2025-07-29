from fastapi import FastAPI

from Payments.Controller.PaymentController import PAYMENT_ROUTER

app = FastAPI(title="Rinha Back-end 2025", description="Implementação da rinha back-end do github.com/gustavoalmeidam7 em FastAPI, SQLAlchemy, asyncpg e uvicorn", version="0.1.0")

@app.on_event("startup")
def startup():
    app.include_router(PAYMENT_ROUTER)
