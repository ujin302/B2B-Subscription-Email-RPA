from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import GPTSubscriptionsTable, EmailsInfoTable
from app.schemas.gpt_subscriptions import GPTSubscriptions
from app.schemas.emails_info import EmailsInfo

# Email 원본 저장
def add_email_data(email_list: list[EmailsInfo], db: Session):
    try:
        email_list = [EmailsInfoTable(**sub.model_dump()) for sub in email_list]
        db.add_all(email_list)
        db.commit()
        return email_list # model 객체 반환
    except IntegrityError as ie:
        db.rollback()
        print('예외 발생하여 rollback 실행')
        print('Email 원본 저장 시, uid 값이 중복되어 예외 발생했습니다.')
        print(f'예외 메세지: {ie}')
        raise
    except Exception as e:
        db.rollback()
        print('예외 발생하여 rollback 실행')
        print(f'예외 메세지 {e}')
        raise


# GPT 답변 리스트 저장
def add_gpt_response(gpt_list: list[GPTSubscriptions], db: Session):
    try:
        gpt_model_list = [GPTSubscriptionsTable(**sub.model_dump()) for sub in gpt_list]
        db.add_all(gpt_model_list)
        db.commit()
        return gpt_model_list # model 객체 반환
    except Exception as e:
        db.rollback()
        print('예외 발생하여 rollback 실행')
        print(f'예외 메세지 {e}')
        raise


# 가장 마지막에 받은 메일의 uid 추출
def get_last_email_uid(db: Session):
    try:
        last_email = db.query(EmailsInfoTable).order_by(EmailsInfoTable.email_date).first()
        return last_email.uid if last_email else None
    except Exception as e:
        db.rollback()
        print('예외 발생하여 rollback 실행')
        print(f'예외 메세지 {e}')
        raise