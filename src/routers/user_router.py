from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.database.core import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.models import User
from src.dependencies.auth_dependencies import check_auth
from src.schemas.user_schemas import RegisterRequest
from src.services.auth_session_service import refresh_session
from src.services.user_service import delete_user, promote_user, register_user

router = APIRouter()

@router.post("/register", tags=["User"])
async def register(register_request: RegisterRequest, res: Response, db: Session = Depends(get_db)):
   new_user = register_user(db, register_request.username, register_request.password)
   if new_user:    
        session = refresh_session(new_user, db)
        res.set_cookie("sessionId", session.id)
        return {"detail": "Succesfully registered user.", "user": new_user.get_user_public()}
   else: 
        raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f'Failed to register user.'
        )

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