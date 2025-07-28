from app.services import mail_service
from app.services import gptapi_service

# 1. 메일 추출
# 2. 청약 데이터 추출(gpt api 사용)
# 3. uipath 실행
def start():
    mail_list = mail_service.get_email_list()
    gpt_list = gptapi_service.ask_gpt(mail_list)
    return gpt_list