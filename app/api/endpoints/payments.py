from fastapi import APIRouter
from app.schemas.payments import (
    CreatePaymentSchema,
    PaymentResponseSchema
)
from app.CRMRequests.payments import create_payment

api = APIRouter()


@api.post("/", response_model=PaymentResponseSchema, status_code=201)
async def create_new_payment(payment: CreatePaymentSchema):
    """ Create and link a new payment for an order """
    return await create_payment(payment)
