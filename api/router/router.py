from fastapi import APIRouter

data_router = APIRouter(
    prefix="/data",
    tags=["Get data"]
)

create_data = APIRouter(
    prefix="/create",
    tags=["Add data"]
)