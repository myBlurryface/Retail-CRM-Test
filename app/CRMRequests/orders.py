import httpx
import json
import os
from dotenv import load_dotenv

from app.schemas.orders import (
    CreateOrderSchema,
    OrderInfoResponseSchema,
    OrderItemSchema
)
from fastapi import HTTPException
from typing import List

load_dotenv()

RETAILCRM_API_KEY = os.environ.get("RETAILCRM_API_KEY")
RETAILCRM_URL = os.environ.get("RETAILCRM_URL")


async def get_client_orders(client_id: int) -> List[OrderInfoResponseSchema]:
    """ Get list of client orders """
    async with httpx.AsyncClient() as client:
        params = {"apiKey": RETAILCRM_API_KEY, "filter[customerId]": client_id}
        response = await client.get(f"{RETAILCRM_URL}/orders", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error getting orders")

        data = response.json()
        return [
            OrderInfoResponseSchema(
                id=order["id"],
                client_id=order.get("customer", {}).get("id"),
                order_number=order["number"],
                createdAt=order.get("createdAt"),
                items=[
                    OrderItemSchema(
                        product_id=item.get("offer", {}).get("id", order["id"]),
                        product_name=item.get("offer", {}).get("name"),
                        quantity=item["quantity"],
                        price=item["initialPrice"]
                    )
                    for item in order["items"]
                ]
            )
            for order in data.get("orders", [])
        ]


async def create_order(order: CreateOrderSchema) -> OrderInfoResponseSchema:
    """ Create a new order """
    async with httpx.AsyncClient() as client:
        params = {"apiKey": RETAILCRM_API_KEY}
        order_data = {
            "number": order.order_number,
            "items": [
                {
                    """
                    В документации сказано: 
                    В случае, если ни один из идентификаторов товара не передан либо товар не найден, 
                    то товар будет автоматически создан на основе данных полей order[items][][initialPrice], 
                    order[items][][purchasePrice], order[items][][productName], 
                    при этом данная позиция товара в заказе не привязывается к товару в каталоге.
                    
                    По какой-то причине автоматическое создание товара, в случае его отсутвия, не работает и 
                    возвращает ошибку. Новый товар не создается, если указывать id товара. При создании нового товара
                    вместо переданного productName - ставит noname.
                    
                    Возможно я что-то делаю не так, но я не нашел, почему так происходит. А может документация 
                    не актуальна.
                    
                    """
                    #"offer": {"id": item.product_id},
                    "productName": item.product_name,
                    "quantity": item.quantity,
                    "initialPrice": item.price,
                    "purchasePrice": item.price
                }
                for item in order.items
            ]
        }
        if order.client_id:
            order_data["customer"] = {"id": order.client_id}
        elif order.client_email:
            order_data["customer"] = {"email": order.client_email}

        order_json = json.dumps(order_data)
        data = {"order": order_json}

        response = await client.post(
            f"{RETAILCRM_URL}/orders/create",
            params=params,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Error while creating a new order")

        data = response.json()
        created_order = data.get("order", {})
        return OrderInfoResponseSchema(
            id=data.get("id"),
            client_id=created_order.get("customer", {}).get("id"),
            order_number=created_order.get("number"),
            createdAt=created_order.get("createdAt"),
            items=[
                OrderItemSchema(
                    product_id=item.get("offer", {}).get("id", data["id"]),
                    product_name=item.get("offer", {}).get("name"),
                    quantity=item["quantity"],
                    price=item["initialPrice"]
                )
                for item in created_order.get("items", [])
            ]
        )
