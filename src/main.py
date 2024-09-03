from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.database.core import get_db
from src.routers import ticket_router, page_router, user_router, auth_session_router
from src.dependencies.auth_dependencies import AuthRedirect
from src.handlers import auth_redirect_handler
from fastapi_health import health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://127.0.0.1:8000","http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"], # include additional methods as per the application demand
    allow_headers=["Content-Type","Set-Cookie"], # include additional headers as per the application demand
    expose_headers=["Set-Cookie"],
)

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

