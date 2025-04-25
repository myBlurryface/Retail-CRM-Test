import httpx
import json
import os
from dotenv import load_dotenv

from app.schemas.payments import CreatePaymentSchema, PaymentResponseSchema
from fastapi import HTTPException

load_dotenv()

RETAILCRM_API_KEY = os.environ.get("RETAILCRM_API_KEY")
RETAILCRM_URL = os.environ.get("RETAILCRM_URL")


async def create_payment(payment: CreatePaymentSchema) -> PaymentResponseSchema:
    async with httpx.AsyncClient() as client:
        """ Create payment for order """
        params = {"apiKey": RETAILCRM_API_KEY}

        payment_data = {
            "order": {"id": payment.order_id},
            "amount": payment.amount,
            "type": payment.type,
            "status": "paid"
        }

        payment_json = json.dumps(payment_data)
        data = {"payment": payment_json}

        response = await client.post(
            f"{RETAILCRM_URL}/orders/payments/create",
            params=params,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при создании платежа")

        data = response.json()
        return PaymentResponseSchema(
            id=data.get("id"),
        )
