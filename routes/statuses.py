from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Status
from schemas import StatusCreate, StatusResponse
from typing import List
from auth_utils import verify_token  # Middleware xác thực

print("✅ statuses.py has been loaded successfully!")

router = APIRouter()

# 📌 1. API tạo mới một Status
@router.post("/", response_model=StatusResponse)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    existing_status = db.query(Status).filter(Status.name == status.name).first()
    if existing_status:
        raise HTTPException(status_code=400, detail="Status already exists")

    new_status = Status(name=status.name)

    db.add(new_status)
    db.commit()
    db.refresh(new_status)

    return new_status

# 🔐 Yêu cầu Authentication để lấy danh sách Statuses
@router.get("/", response_model=List[StatusResponse])
def get_statuses(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    return db.query(Status).all()

# 📌 3. API lấy thông tin Status theo ID
@router.get("/{status_id}", response_model=StatusResponse)
def get_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

# 📌 4. API cập nhật Status
@router.put("/{status_id}", response_model=StatusResponse)
def update_status(status_id: int, status_update: StatusCreate, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    status.name = status_update.name

    db.commit()
    db.refresh(status)

    return status

# 📌 5. API xóa Status
@router.delete("/{status_id}")
def delete_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    db.delete(status)
    db.commit()

    return {"message": "Status deleted successfully"}
