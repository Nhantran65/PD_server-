from fastapi import FastAPI
from routes.auth import router as auth_router  # Sửa import
from routes.hospitals import router as hospital_router
from routes.statuses import router as statuses_router
from routes.predict import router as predict_router
from routes.examinations import router as examination_router
from routes.profile import router as profile_router
from routes.users import router as user_router
from routes.results import router as results_router
from routes.doctor_decisions import router as doctor_decisions_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(hospital_router, prefix="/hospitals", tags=["Hospitals"])
app.include_router(statuses_router, prefix = "/statuses", tags=["statuses"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(examination_router, prefix="/examinations", tags=["Examinations"])
app.include_router(profile_router, prefix = "/profile", tags = ["Profile"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(results_router, prefix="/results", tags=["Results"])
app.include_router(doctor_decisions_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Medical API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Sửa cách chạy

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi domain truy cập API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Cho phép tất cả headers
)