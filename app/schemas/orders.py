from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, List


class OrderItemSchema(BaseModel):
    """ Schema for items in order """
    product_name: str
    product_id: int
    quantity: int
    price: float


class CreateOrderSchema(BaseModel):
    """ Schema for new order creation """
    client_id: Optional[int] = None
    client_email: Optional[EmailStr] = None
    items: List[OrderItemSchema]
    order_number: str

    @model_validator(mode="after")
    def check_client_info(cls, values):
        if not values.client_id and not values.client_email:
            raise ValueError("You need to point client_id or client_email")
        return values


class OrderInfoResponseSchema(BaseModel):
    """ Schema for order info returning """
    id: int
    client_id: Optional[int] = None
    order_number: str
    createdAt: Optional[str] = None
    items: List[OrderItemSchema]
