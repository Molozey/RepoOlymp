import jwt
from litestar import Response
from litestar.datastructures import ResponseHeader
from litestar import Controller
from litestar import post, get
import time

from backend.middlewares.auth import auth_middleware
from backend.roles import Auditor

from backend.db import ENGINE
import pandas as pd
from pydantic import BaseModel
from backend.logs import create_logger

LOGGER = create_logger(__name__)


class BuyerItem(BaseModel):
    buyer_name: str
    buyer_amount: float


class AuditorController(Controller):
    path = "/auditor"

    middleware = [auth_middleware(roles={Auditor})]

    @get("/test")
    async def test_audior(self) -> dict:
        _ = self
        return {"message": "test", "status": "success"}

    @get("/buyers")
    async def get_buyers(self, builder_id: int) -> list[BuyerItem]:
        results = pd.read_sql(
            f"""
            SELECT * FROM users.users_with_events WHERE builder_id = {builder_id};
        """,
            con=ENGINE(),
        )
        user_results = [
            BuyerItem(buyer_name=item["name"], buyer_amount=item["money"])
            for _, item in results.iterrows()
        ]
        return user_results
