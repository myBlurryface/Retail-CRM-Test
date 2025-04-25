from fastapi import FastAPI
from app.api.api import api

app = FastAPI(
    title="RetailCRM Integration",
    description="API for managing customers and orders via RetailCRM",
    docs_url="/api/retailcrm/docs/",
    openapi_url="/api/retailcrm/openapi.json",
    version="0.0.1",
)

app.include_router(api)
