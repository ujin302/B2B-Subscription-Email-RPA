# app/api/endpoints/start.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.services import start_service

router = APIRouter()

@router.get("/")
def start_subscription_email():
    result = start_service.start()
    return {"mail": result}