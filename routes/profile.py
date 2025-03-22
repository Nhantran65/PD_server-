from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_utils import verify_token
from database import get_db
from models import User
from schemas import UserProfileUpdate, UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserProfileUpdate)
def update_current_user(update_data: UserProfileUpdate, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user