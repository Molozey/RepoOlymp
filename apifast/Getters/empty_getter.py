from fastapi import APIRouter
from pydantic import BaseModel
from dataclasses import dataclass
from apifast.logs import create_logger
import pandas as pd
from apifast.db import ENGINE

LOGGER = create_logger(__name__)
router = APIRouter(prefix="/testing", tags=["tests"])


class EmptyResp(BaseModel):
    integer: int
    text: str


@router.get("")
async def get_empty(integer: int = 0) -> EmptyResp:
    LOGGER.info("Called get empty")
    return EmptyResp(integer=integer, text="empty")


@router.get("/unknown")
async def get_unknown():
    return {"message": "unknown", "status_code": 200}

#
@router.get("/pop")
async def pop():
    return {"message": "unknown"}

@router.get("/database")
async def db_check():
    return pd.read_sql("SELECT * FROM positions.table_1", con=ENGINE()).to_dict("records")