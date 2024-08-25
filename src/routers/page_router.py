from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.schemas.user_schemas import UserPublic
from src.services.ticket_service import get_user_tickets
from src.database.models import User
from src.dependencies.auth_dependencies import check_auth_redirect, get_user_public

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def home(req: Request, user_public: User = Depends(get_user_public)):
    return templates.TemplateResponse(
        request=req, name="/pages/home.html", context={"page": "/", "user": user_public}
    )

@router.get("/my-tickets-page", tags=["Pages"], dependencies=[Depends(check_auth_redirect)])
async def view_my_tickets(req: Request, user_public: UserPublic = Depends(get_user_public), db: Session = Depends(get_db)):
    tickets = get_user_tickets(db, user_public.id)
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets.html", context={"page": "/my-tickets-page", "tickets": tickets, "user": user_public}
    )

@router.get("/unauthorised-page", tags=["Pages"])
async def unauthorised(req: Request, old_location: str = Query("old_location"), user_public: UserPublic = Depends(get_user_public)):
    return templates.TemplateResponse(
        request=req, name="/pages/unauthorised.html", context={"page": old_location, "user": user_public}
    )