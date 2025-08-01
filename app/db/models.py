from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from app.db.base import Base
from datetime import datetime

# 메일 원본 정보
class EmailsInfoTable(Base):
    __tablename__ = "emails_info"

    pk = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(String(255), unique=True, nullable=False)
    from_addr = Column(String(255), nullable=False)
    to_addr = Column(String(255), nullable=False)
    email_date = Column(String(100), nullable=False)
    subject = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    processed_date = Column(DateTime, default=datetime.utcnow)


# GPT 추출 결과
class GPTSubscriptionsTable(Base):
    __tablename__ = "gpt_subscriptions"

    pk = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_uid = Column(String(255), ForeignKey("emails_info.uid"), nullable=False)
    is_subscription = Column(Boolean, default=False, nullable=False)
    company_name = Column(String(255))
    contact_name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    service_name = Column(String(255))
    quantity = Column(Integer)
    installation_date = Column(String(50))
    address = Column(String(500))
    contract_type = Column(String(50))
    additional_request = Column(Text)
    processed_date = Column(DateTime, default=datetime.utcnow)


# RPA 실행 결과
class RPAResultsTable(Base):
    __tablename__ = "rpa_results"

    pk = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gpt_pk = Column(Integer, ForeignKey("gpt_subscriptions.pk"), nullable=False)
    status = Column(String(50), nullable=False)  # SUCCESS / FAIL
    excel_name = Column(String(200), nullable=False)
    processed_date = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text)