from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.handlers.auth_redirect_handler import AuthRedirect
from src.services.ticket_service import get_ticket_by_id, get_user_tickets, get_all_unresolved_tickets
from src.database.models import User
from src.dependencies.auth_dependencies import check_auth_redirect, get_user
from src.services.user_service import get_public_users

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def home(req: Request, user: User = Depends(get_user)):
    return templates.TemplateResponse(
        request=req, name="/pages/home.html", context={"page": "/", "user": user.get_user_public() if user else None }
    )

@router.get("/my-tickets-page", tags=["Pages"], dependencies=[Depends(check_auth_redirect)])
async def view_my_tickets(req: Request, user: User = Depends(get_user), db: Session = Depends(get_db)):
    user_tickets = get_user_tickets(db, user.id)
    tickets_to_review = []
    if(user.is_admin): tickets_to_review = get_all_unresolved_tickets(db, user.id) 
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets.html", context={"page": "/my-tickets-page", "user_tickets": user_tickets, "tickets_to_review": tickets_to_review, "user": user.get_user_public() if user else None }
    )

@router.get("/admin-dashboard-page", tags=["Pages"], dependencies=[Depends(check_auth_redirect)])
async def admin_dashboard(req: Request, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if(user.is_admin == False): raise AuthRedirect
    other_users_details = get_public_users(db)
    return templates.TemplateResponse(
        request=req, name="/pages/admin_dashboard.html", context={"page": "/admin-dashboard-page", "user": user.get_user_public() if user else None, "other_users_details": other_users_details}
    )

@router.get("/view-ticket-page/{ticket_id}", tags=["Pages"], dependencies=[Depends(check_auth_redirect)])
async def view_ticket(req: Request, ticket_id: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    ticket = get_ticket_by_id(db, ticket_id, user.get_user_public)
    if ticket != None: ticket = ticket.get_ticket_public()
    if(ticket != None and (ticket.author.id != user.id and user.is_admin == False)): raise AuthRedirect
    return templates.TemplateResponse(
        request=req, name="/pages/view_ticket.html", context={"page": f'/view-ticket-page/{ticket_id}', "user": user.get_user_public() if user else None, "ticket": ticket }
    )

@router.get("/unauthorised-page", tags=["Pages"])
async def unauthorised(req: Request, old_location: str = Query("old_location"), user: User = Depends(get_user)):
    return templates.TemplateResponse(
        request=req, name="/pages/unauthorised.html", context={"page": old_location, "user": user.get_user_public() if user else None }
    )