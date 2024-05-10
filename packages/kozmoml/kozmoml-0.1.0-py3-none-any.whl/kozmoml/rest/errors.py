from typing import Optional
from fastapi import Request
from pydantic import BaseModel

from .responses import Response
from ..errors import KozmoMLError


class APIErrorResponse(BaseModel):
    error: Optional[str] = None


async def handle_kozmoml_error(request: Request, exc: KozmoMLError) -> Response:
    err_res = APIErrorResponse(error=str(exc))
    return Response(status_code=exc.status_code, content=err_res.dict())


_EXCEPTION_HANDLERS = {KozmoMLError: handle_kozmoml_error}
