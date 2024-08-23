from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers import ticket_router, page_router, user_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router.router)
app.include_router(ticket_router.router)
app.include_router(user_router.router)