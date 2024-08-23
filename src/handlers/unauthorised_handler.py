from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

async def handler(request: Request, exc: RuntimeError) -> JSONResponse:
    return RedirectResponse("/unauthorised-page")