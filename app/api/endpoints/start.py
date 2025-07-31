# app/api/endpoints/start.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.services import start_service

router = APIRouter()

@router.get("/")
def start_subscription_email(db: Session = Depends(get_db)):
    try:
        return start_service.start(db)
    except Exception as e:
        print('endpoint: /start & method: get에서 오류 발생했습니다.')
        print(f'오류 메세지: {e}')
        return HTTPException(status_code=400, detail=(e))