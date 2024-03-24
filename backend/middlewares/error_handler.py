from litestar import Request
from litestar import Response
from litestar.status_codes import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from litestar import MediaType
from backend.logs import create_logger

LOG = create_logger(__name__)


def error_handler(request: Request, exception: Exception) -> Response:
    """
    Handle possible errors
    :param request:
    :param exception:
    :return:
    """
    _ = request
    error = str(exception)
    LOG.error(f"Error while processing request: {error}", exc_info=True)
    status_code = HTTP_500_INTERNAL_SERVER_ERROR

    return Response(
        media_type=MediaType.TEXT,
        content=f"Error while processing request caused by {exception.__class__.__name__} \n{error}",
        status_code=status_code,
    )