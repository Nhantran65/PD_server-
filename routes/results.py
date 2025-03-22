# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from models import Result
# from schemas import ResultCreate, ResultResponse
# from typing import List

# router = APIRouter()

# # 🔹 1. API Tạo kết quả dự đoán
# @router.post("/", response_model=ResultResponse)
# def create_result(result: ResultCreate, db: Session = Depends(get_db)):
#     new_result = Result(**result.dict())
#     db.add(new_result)
#     db.commit()
#     db.refresh(new_result)
#     return new_result

# # 🔹 2. API Lấy danh sách tất cả kết quả
# @router.get("/", response_model=List[ResultResponse])
# def get_results(db: Session = Depends(get_db)):
#     return db.query(Result).all()

# # 🔹 3. API Lấy kết quả theo ID
# @router.get("/{result_id}", response_model=ResultResponse)
# def get_result(result_id: int, db: Session = Depends(get_db)):
#     result = db.query(Result).filter(Result.id == result_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Result not found")
#     return result

# # 🔹 4. API Cập nhật kết quả (chỉ cập nhật `doctor_decision`)
# @router.put("/{result_id}", response_model=ResultResponse)
# def update_result(result_id: int, doctor_decision: bool, db: Session = Depends(get_db)):
#     result = db.query(Result).filter(Result.id == result_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Result not found")

#     result.doctor_decision = doctor_decision
#     db.commit()
#     db.refresh(result)
#     return result

# # 🔹 5. API Xóa kết quả
# @router.delete("/{result_id}")
# def delete_result(result_id: int, db: Session = Depends(get_db)):
#     result = db.query(Result).filter(Result.id == result_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Result not found")

#     db.delete(result)
#     db.commit()
#     return {"message": "Result deleted successfully"}
