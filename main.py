# main.py
from fastapi import FastAPI
from app.api.routers import api_router as start_router
from app.db.base import Base, engine
from app.db import models

# Fast API 인스턴스 생성
app = FastAPI()

# 라우터 등록
app.include_router(start_router)

# table 생성
Base.metadata.create_all(engine)