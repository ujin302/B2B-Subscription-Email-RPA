# main.py
from fastapi import FastAPI
from app.api.routers import api_router as start_router

# Fast API 인스턴스 생성
app = FastAPI()

# 라우터 등록
app.include_router(start_router)