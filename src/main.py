from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.database.core import get_db
from src.routers import ticket_router, page_router, user_router, auth_session_router
from src.dependencies.auth_dependencies import AuthRedirect
from src.handlers import auth_redirect_handler
from fastapi_health import health

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router.router)
app.include_router(prefix="/tickets", router=ticket_router.router)
app.include_router(prefix="/users", router=user_router.router)
app.include_router(prefix="/auth-sessions", router=auth_session_router.router)

def is_database_online(session: bool = Depends(get_db)):
    return session
app.add_api_route("/health", health([is_database_online]))

app.add_exception_handler(AuthRedirect, auth_redirect_handler.handler)

