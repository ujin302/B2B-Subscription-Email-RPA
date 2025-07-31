from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# gpt가 분석한 청약 정보
class GPTSubscriptions(BaseModel):
    pk : Optional[int] = None
    email_uid : str # 메일 UID
    is_subscription : bool # 청약 메일 여부
    company_name : Optional[str] = None # 고객사명
    contact_name : Optional[str] = None # 고객사측 담당자
    phone : Optional[str] = None # 연락처
    email : Optional[str] = None # 이메일
    service_name : Optional[str] = None # 신청 서비스 
    quantity : Optional[int] = None # 회선 수
    installation_date : Optional[str] = None # 설치 희망일 (YYYY-MM-dd)
    address : Optional[str] = None # 설치 주소
    contract_type : Optional[str] = None # 계약 유형
    additional_request : Optional[str] = None # 추가 요청 사항
    processed_date: Optional[datetime] = None # DB에 저장된 시각
    
    class Config:
        from_attributes = True # ORM 객체에서 속성 읽기 허용