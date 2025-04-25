from fastapi import APIRouter
from app.api.endpoints import (
        clients,
        orders,
        payments,
)

api = APIRouter()

api.include_router(clients.api, tags=["Clients"], prefix="/api/clients")
api.include_router(orders.api, tags=["Orders"], prefix="/api/orders")
api.include_router(payments.api, tags=["Payments"], prefix="/api/payments")
