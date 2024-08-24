from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

async def handler(request: Request, exc: RuntimeError) -> JSONResponse:
    query_params = {"old_location": request.url.path}
    redirect_url = f"/unauthorised-page?{urlencode(query_params)}"
    return RedirectResponse(redirect_url)