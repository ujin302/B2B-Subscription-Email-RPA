# app/api/routers.py
from fastapi import APIRouter
from app.api.endpoints import start

# 여러 api 묶기
api_router = APIRouter()

# 엔드포인트 설정
api_router.include_router(start.router, prefix="/start", tags = ["start"])