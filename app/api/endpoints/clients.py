from fastapi import APIRouter, Depends
from app.schemas.clients import (
    CreateNewClientSchema,
    ClientInfoResponseSchema,
    ClientsFilterSchema,
    ClientsListInfoResponseSchema,
)
from app.CRMRequests.clients import get_clients, create_client
from typing import List

api = APIRouter()


@api.get("/", response_model=List[ClientsListInfoResponseSchema])
async def list_customers(filters: ClientsFilterSchema = Depends()):
    """
    Retrieve a list of customers from RetailCRM with optional filters.
    """
    return await get_clients(filters)


@api.post("/", response_model=ClientInfoResponseSchema, status_code=201)
async def create_new_client(client: CreateNewClientSchema):
    """
    Create a new customer in RetailCRM.
    """
    return await create_client(client)
