from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import UserOut
from app.crud.user import list_users, get_user_by_id
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("", response_model=list[UserOut])
def users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def user_detail(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user