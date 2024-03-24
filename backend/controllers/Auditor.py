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


class AuditorController(Controller):
    path = "/auditor"

    middleware = [
        auth_middleware(roles={
            Auditor
        })
    ]

    @get("/test")
    async def test_audior(self) -> dict:
        _ = self
        return {"message": "test", "status": "success"}