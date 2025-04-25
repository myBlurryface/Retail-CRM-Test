import httpx
import json
import os
from dotenv import load_dotenv

from app.schemas.clients import (
    CreateNewClientSchema,
    ClientInfoResponseSchema,
    ClientsFilterSchema,
    ClientsListInfoResponseSchema,
)
from typing import List
from fastapi import HTTPException
from datetime import datetime

load_dotenv()

RETAILCRM_API_KEY = os.environ.get("RETAILCRM_API_KEY")
RETAILCRM_URL = os.environ.get("RETAILCRM_URL")


async def get_clients(filters: ClientsFilterSchema) -> List[ClientInfoResponseSchema]:
    """ Get customers from RetailCRM with/without filters """
    async with httpx.AsyncClient() as client:
        params = {"apiKey": RETAILCRM_API_KEY}
        if filters.firstName:
            params["filter[name]"] = filters.firstName
        if filters.email:
            params["filter[email]"] = filters.email

        start_date = filters.register_date_start
        end_date = filters.register_date_end
        if end_date:
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        response = await client.get(f"{RETAILCRM_URL}/customers", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching customers from RetailCRM")

        # Filter by date of creation
        data = response.json()
        result = []
        for customer in data.get("customers", []):
            print(customer)
            created_at_str = customer.get("createdAt")
            include_customer = True

            if created_at_str and (filters.register_date_start or filters.register_date_end):
                try:
                    created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                if start_date and created_at < start_date:
                    include_customer = False
                if end_date and created_at > end_date:
                    include_customer = False

            if include_customer:
                result.append(
                    ClientsListInfoResponseSchema(
                        id=customer["id"],
                        name=customer.get("firstName", "Unknown User"),
                        email=customer.get("email", "unknown@email.ru"),
                        createdAt=created_at_str
                    )
                )

        return result


async def create_client(new_client: CreateNewClientSchema) -> ClientInfoResponseSchema:
    """ Create a new client in RetailCRM """
    async with httpx.AsyncClient() as client:
        params = {"apiKey": RETAILCRM_API_KEY}

        customer_data = {
            "firstName": new_client.firstName,
            "email": new_client.email,
        }

        if new_client.phone:
            customer_data["phone"] = new_client.phone

        customer_json = json.dumps(customer_data)

        data = {
            "customer": customer_json
        }

        response = await client.post(
            f"{RETAILCRM_URL}/customers/create",
            params=params,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Error creating customer in RetailCRM")

        data = response.json()
        return ClientInfoResponseSchema(
            id=data.get("id")
        )
