from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers import ticket_router, page_router, user_router
from src.dependencies.auth_dependencies import AuthRedirect
from src.handlers import auth_redirect_handler
from src.dependencies.auth_dependencies import get_user_public

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(page_router.router)
app.include_router(ticket_router.router)
app.include_router(user_router.router)
app.add_exception_handler(AuthRedirect, auth_redirect_handler.handler)