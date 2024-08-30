from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.handlers.auth_redirect_handler import AuthRedirect
from src.schemas.user_schemas import UserPublic
from src.services.ticket_service import get_user_tickets, get_all_unresolved_tickets
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
    user_tickets = get_user_tickets(db, user_public.id)
    tickets_to_review = []
    if(user_public.is_admin): tickets_to_review = get_all_unresolved_tickets(db, user_public.id) 
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets.html", context={"page": "/my-tickets-page", "user_tickets": user_tickets, "tickets_to_review": tickets_to_review, "user": user_public}
    )

@router.get("/admin-dashboard-page", tags=["Pages"], dependencies=[Depends(check_auth_redirect)])
async def admin_dashboard(req: Request, user_public: UserPublic = Depends(get_user_public), db: Session = Depends(get_db)):
    if(user_public.is_admin == False): raise AuthRedirect
    return templates.TemplateResponse(
        request=req, name="/pages/admin_dashboard.html", context={"page": "/admin-dashboard-page", "user": user_public}
    )

@router.get("/unauthorised-page", tags=["Pages"])
async def unauthorised(req: Request, old_location: str = Query("old_location"), user_public: UserPublic = Depends(get_user_public)):
    return templates.TemplateResponse(
        request=req, name="/pages/unauthorised.html", context={"page": old_location, "user": user_public}
    )