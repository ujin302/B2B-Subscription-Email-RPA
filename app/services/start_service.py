import subprocess
import os

from sqlalchemy.orm import Session

from app.db.crud import *
from app.services import email_service, gptapi_service, excel_service
from app.schemas.gpt_subscriptions import GPTSubscriptions

# 1. 메일 추출
# 2. 청약 데이터 추출(gpt api 사용)
# 3. 엑셀에 저장
# 4. uipath 실행
def start(db: Session):
    # 1. 메일 추출
    uid = get_last_email_uid(db)
    email_list = email_service.get_email_list(uid)
    if len(email_list) is 0: 
        return "새로운 메일이 없습니다."
    add_email_data(email_list, db) # Email 원본 DB 저장
    
    # 2. 청약 데이터 추출(gpt api 사용)
    gpt_list = gptapi_service.ask_gpt(email_list)
    db_list = add_gpt_response(gpt_list, db) # GPT 응답 DB 저장
    # GPTSubscriptions > Pydantic 객체: 데이터 검증 & 직렬화
    # 따라서 Model를 검증할 필요가 있어 model_validate() 함수 사용
    gpt_json_list = [GPTSubscriptions.model_validate(m).model_dump() for m in db_list]
    
    # 3. 엑셀에 저장
    excel_name = excel_service.write_data(gpt_json_list)
    
    # 4. Uipath 실행
    rpa_result = start_uipath()
    return {"gpt_list": gpt_json_list, "excel_name": excel_name, "rpa_result": rpa_result}


def start_uipath():
    uirobot_path = os.getenv("UIROBOT_PATH")
    rpa_nupkg = os.getenv("RPA_NUPKG")
    
    result = subprocess.run([uirobot_path, "execute", "--file", rpa_nupkg])
    
    if result.returncode == 0:
        print("UiPath 프로젝트 실행 성공")
        return "실행 성공"
    else: 
        print("실패: ", result.returncode)
        return f"실행 실패: {result.returncode}"