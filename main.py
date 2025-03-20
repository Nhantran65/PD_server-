from fastapi import FastAPI
from routes.auth import router as auth_router  # Sửa import
from routes.hospitals import router as hospital_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(hospital_router, prefix="/hospitals", tags=["Hospitals"])

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
    allow_methods=["*"],  # Cho phép tất cả các method (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Cho phép tất cả headers
)