from fastapi import APIRouter
from app.schemas.orders import CreateOrderSchema, OrderInfoResponseSchema
from app.CRMRequests.orders import (
    get_client_orders,
    create_order,
)
from typing import List

api = APIRouter()


@api.get("/{client_id}/", response_model=List[OrderInfoResponseSchema])
async def list_client_orders(client_id: int):
    """ Get list of client's orders """
    return await get_client_orders(client_id)


@api.post("/", response_model=OrderInfoResponseSchema, status_code=201)
async def create_new_order(order: CreateOrderSchema):
    """ Creation of new orders. Look into code comments of CRMRequests.orders module about product id. """
    return await create_order(order)
