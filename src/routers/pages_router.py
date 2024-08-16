from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def view_tickets(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request, name="hello-world.html"
    )