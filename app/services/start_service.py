from app.services import mail_service

# 1. 메일 추출
# 2. 청약 데이터 추출(gpt api 사용)
# 3. uipath 실행
def start():
    mailList = mail_service.getEmailList()
    return mailList