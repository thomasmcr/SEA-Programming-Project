from fastapi import APIRouter, Depends, HTTPException, status
from src.database.core import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.models import User
from src.dependencies.auth_dependencies import check_auth
from src.services.user_service import delete_user, promote_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/register", tags=["User"])
async def register(db: Session = Depends(get_db)):
   return {"message": "not implemented yet!"}

@router.delete("/{user_id}", tags=["User"])
async def delete(user_id: str, db: Session = Depends(get_db), user: User = Depends(check_auth)):
    deleted_user = delete_user(db, user_id, user)
    if deleted_user:
        return {"detail": "Succesfully deleted user.", "user": deleted_user}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to delete user with id {user_id}. Please try again.'
        )
      
@router.put("/promote/{user_id}", tags=["User"])
async def promote(user_id: str, db: Session = Depends(get_db), user: User = Depends(check_auth)):
    promoted_user = promote_user(db, user_id, user)
    if promoted_user:
        return {"detail": "Succefully promoted user.", "user": promoted_user}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to promote user with id {user_id}. Please try again.'
        )