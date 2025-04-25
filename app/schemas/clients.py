from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import datetime


class CreateNewClientSchema(BaseModel):
    """ Add new client to CRM """
    firstName: str
    email: EmailStr
    phone: str


class ClientInfoResponseSchema(BaseModel):
    """ Response schema after creation """
    id: int


class ClientsListInfoResponseSchema(ClientInfoResponseSchema):
    name: str
    email: EmailStr
    createdAt: datetime


class ClientsFilterSchema(BaseModel):
    """ Get list of clients with filters """
    firstName: Optional[str] = None
    email: Optional[EmailStr] = None
    register_date_start: Optional[datetime] = None
    register_date_end: Optional[datetime] = None

    @model_validator(mode="after")
    def check_date_range(cls, values):
        start_date = values.register_date_start
        end_date = values.register_date_end
        if start_date and end_date and start_date > end_date:
            raise ValueError("register_date_start cannot be later than register_date_end")
        return values
