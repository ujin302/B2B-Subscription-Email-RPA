from dotenv import load_dotenv
import os
import re
from datetime import datetime

import imaplib
import email
from email.header import decode_header, make_header

from app.schemas.emails_info import EmailsInfo

# .env에서 정보 가져오기    
user = os.getenv("GMAIL_USER")
password =  os.getenv("GMAIL_PW")

# 메일 정제
def clean_email_text(text: str) -> str:
    # 1. \r\n → \n
    text = text.replace("\r\n", "\n")

    # 2. HTML 태그 제거
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)  # <>로 감싼 링크만
    text = re.sub(r"\[image:.*?\]", "", text)  # [image: Google] 제거

    # 3. 공백 줄 정리
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()

# 메일 리스트 추출 
def get_email_list(last_uid):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)

    #받은 편지함에서 검색
    imap.select("INBOX")
    if last_uid is None:
        status, data = imap.uid('search', None, 'ALL') # 모든 메일
    else:
        status, data = imap.uid('search', None, f'(UID {last_uid}:*)') # UID 범위 지정
        
    
    all_email = data[0].split()
    
    # 최근 메일이 없는 경우 [] 반환
    if len(all_email) is 0 and all_email[0].decode():
        return []
    
    # all_email.reverse()
    all_email_info = []
    for mail in all_email:
        all_email_info.append(get_email_info(mail, imap))
    
    imap.close()
    imap.logout()
    return all_email_info

# 메일 정보 추출
def get_email_info(mail, imap):
    result, data = imap.uid('fetch', mail, '(RFC822)')
    rawEmail = data[0][1]
    email_msg= email.message_from_bytes(rawEmail)
    
    # 메일 정보
    email_info = EmailsInfo(
        uid =  mail.decode(),
        from_addr = str(make_header(decode_header(email_msg.get('From')))),
        to_addr = email_msg['To'],
        email_date = email_msg['Date'],
        subject = str(make_header(decode_header(email_msg.get('Subject')))),
        content = "",
        processed_date = datetime.now()
    )
     
    if email_msg.is_multipart():
        for part in email_msg.get_payload():
            bytes = part.get_payload(decode=True)
            encode = part.get_content_charset()
            content = str(bytes, encode)
            email_info.content = clean_email_text(content)
            break
    
    print(email_info)
    return email_info