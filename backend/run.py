from backend.logs import create_logger
from backend.controllers.auth import AuthController
from backend.controllers.Auditor import AuditorController
from backend.controllers.Testing import TestingController
from litestar import Litestar
from litestar.params import Parameter
from litestar.openapi import OpenAPIConfig
import uvicorn
import os

LOGGER = create_logger(__name__)

def app():
    LOGGER.info("Starting app")
    return Litestar(
        debug=True,
        route_handlers=[
            AuthController,
            AuditorController,
            TestingController,
        ],
        openapi_config=OpenAPIConfig(
            title="AuthService", version="0.0.1", description="AuthService API"
        ),
        parameters={"token": Parameter(description="token", header="X-AUTH-TOKEN")}
    )


def main():
    """Run fastapi service"""
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=int(os.getenv("LITESTAR_API_PORT", "10000")),
        reload=True,
    )


if __name__ == "__main__":
    main()
