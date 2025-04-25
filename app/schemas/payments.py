from pydantic import BaseModel


class CreatePaymentSchema(BaseModel):
    """ Schema for payment creation """
    order_id: int
    amount: float
    type: str


class PaymentResponseSchema(BaseModel):
    """ Response schema of successfull creation """
    id: int
