import jwt
from litestar import Response
from litestar.datastructures import ResponseHeader
from litestar import Controller
from litestar import post
import time

from backend.db import ENGINE
import pandas as pd
from pydantic import BaseModel


JWT_SECRET='mystrong_secret'

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthPipeline(BaseModel):
    token: str
    success: bool


class AuthController(Controller):
    path = "/auth"

    @post(path="/", response_headers=[
        ResponseHeader(
            name="x-auth-token",
            description="jwt-token",
            documentation_only=True
        )
    ])
    async def authenticate(self, data: AuthRequest) -> Response[AuthPipeline]:
        _ = self
        token_body = await check_user_exist(data.username, data.password)
        return Response(content=token_body, headers={'x-user-token': token_body.token})

async def check_user_exist(username: str, password: str) -> AuthPipeline:
    user_info = pd.read_sql(sql=f"""SELECT * FROM platform.user_with_roles WHERE login='{username}' AND password='{password}'""", con=ENGINE())
    print(user_info)
    if user_info.empty:
        return AuthPipeline(token="", success=False)
    else:
        user_roles = list(set(user_info["role_name"]))
        user_id = int(user_info["user_id"].iloc[0])
        token = await _sign_jwt(user_id=user_id, user_roles=user_roles)
        return AuthPipeline(token=token, success=True)

async def _sign_jwt(user_id: int, user_roles:list[str]) -> str:
    token = {
        "user_id": user_id,
        "user_roles": user_roles,
        "expires": time.time() + 10 * 60 # 10 mins
    }
    token = jwt.encode(token, JWT_SECRET, algorithm="HS256")
    return token

