import dataclasses
import os
import time
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Tuple

import jwt
from litestar import Request
from litestar import Response
from litestar.datastructures import Headers
from litestar.middleware import MiddlewareProtocol
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from litestar.types import Receive
from litestar.types import Scope
from litestar.types import Send

from backend.logs import create_logger

LOG = create_logger(__name__)

AUTH_TOKEN_HEADER = "X-AUTH_TOKEN"
TOKEN_STATE = "token"
AUTH_TOKEN_EXPIRES = "10"
ROLES_STATE = "roles"

USER_STATE = "user"
USER_ID_STATE = "-1"
WITHOUT_AUTH_STATE = os.getenv("ALLOW_TO_CALL_WITHOUT_AUTH", True)
JWT_SECRET='mystrong_secret'

@dataclasses.dataclass
class AuthState:
    user_id: str
    token: str
    token_expires_int: Optional[int]
    roles: list[str]


class AuthMiddleware(MiddlewareProtocol):
    def __init__(self, app, roles: Optional[set] = None, can_call_without_auth=False):
        self.app = app
        self.roles = roles if roles else set()
        self.can_call_without_auth = WITHOUT_AUTH_STATE

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        response = self.app
        auth_status, errors = self._make_auth(scope)
        print(auth_status)
        state = scope["app"].state
        state[USER_STATE] = "unknown"
        state[ROLES_STATE] = set()
        auth_success = False
        if auth_status is not None:
            state[ROLES_STATE] = auth_status.roles
            state[USER_ID_STATE] = auth_status.user_id
            state[TOKEN_STATE] = auth_status.token
            state[AUTH_TOKEN_EXPIRES] = auth_status.token_expires_int

            auth_success, errors = self._check_user_roles_enough(auth_status, scope)

        if self.can_call_without_auth:
            auth_success = True

        if not auth_success:
            response = Response(f"Auth failed: {errors}", status_code=HTTP_401_UNAUTHORIZED).to_asgi_response(
                scope["app"],
                Request(scope=scope, receive=receive, send=send)
            )
        await response(scope, receive, send)


    def _check_user_roles_enough(
        self, auth_status: AuthState, scope: "Scope"
    ) -> tuple[bool, str]:
        need_roles = self.roles or scope["route_handler"].opt.get("roles", set())

        if set(need_roles) & set(auth_status.roles):
            return True, "User have required roles"
        else:
            return False, "Need to have at least one role from {}".format(need_roles)

    def _make_auth(self, scope: Scope) -> Tuple[Optional[AuthState], Optional[str]]:
        token = Headers.from_scope(scope).getone("X-AUTH-TOKEN", None)
        auth_state, message = self._decode_token(token)
        if auth_state is None:
            return None, message
        else:
            return auth_state, message

    def _decode_token(self, token: bytes) -> Tuple[Optional[AuthState], str]:
        _t = str(token)
        try:
            token = jwt.decode(token, os.getenv("JWT_SECRET", JWT_SECRET), algorithms=["HS256"])
        except Exception as e:
            LOG.error("Failed to decode token", exc_info=True)
            return None, "Failed to decode token"

        if token["expires"] <= time.time():
            return None, f"Token has expired"

        return AuthState(
            roles=token.get("user_roles", {}),
            user_id=token.get("user_id", "-1"),
            token_expires_int=token["expires"],
            token=_t,
        ), "All is OK"



def auth_middleware(**kwargs) -> Callable:
    def build(app: "ASGIApp"):
        return AuthMiddleware(app, **kwargs)

    return build