from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# RPA(UiPath) 결과 기록
class RPAResults(BaseModel):
    pk : Optional[int] = None
    gpt_pk : int
    status : str
    excel_name : str
    processed_date: datetime # 실행 시작
    error_message : Optional[str] = None