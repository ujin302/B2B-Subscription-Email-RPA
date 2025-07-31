from sqlalchemy.orm import Session

from app.db.crud import *
from app.services import email_service
from app.services import gptapi_service
from app.schemas.gpt_subscriptions import GPTSubscriptions

# 1. 메일 추출
# 2. 청약 데이터 추출(gpt api 사용)
# 3. uipath 실행
def start(db: Session):
    uid = get_last_email_uid(db)
    email_list = email_service.get_email_list(uid)
    if len(email_list) is 0: 
        return "새로운 메일이 없습니다."
    add_email_data(email_list, db) # Email 원본 DB 저장
    
    gpt_list = gptapi_service.ask_gpt(email_list)
    db_list = add_gpt_response(gpt_list, db) # GPT 응답 DB 저장
    # GPTSubscriptions > Pydantic 객체: 데이터 검증 & 직렬화
    # 따라서 Model를 검증할 필요가 있어 model_validate() 함수 사용
    return [GPTSubscriptions.model_validate(m).model_dump() for m in db_list]