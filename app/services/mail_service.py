from dotenv import load_dotenv
import os
import re

import imaplib
import email
from email.header import decode_header, make_header

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
def get_email_list():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)

    imap.select("INBOX")
    #받은 편지함 모든 메일 검색
    status, data = imap.uid('search', None, 'ALL')

    all_email = data[0].split()
    all_email.reverse()
    all_email_info = []
    
    for mail in all_email:
        all_email_info.append(get_email_info(mail, imap))
    
    imap.close()
    imap.logout()
    return all_email_info

# 메일 정보 추출
def get_email_info(mail, imap):
    email_info = {} # 메일 정보 저장
    
    result, data = imap.uid('fetch', mail, '(RFC822)')
    rawEmail = data[0][1]
    email_msg= email.message_from_bytes(rawEmail)
    
    # 메일 정보
    email_info['UID'] = mail.decode()
    email_info['FROM'] = str(make_header(decode_header(email_msg.get('From'))))
    email_info['SENDER'] = email_msg['Sender']
    email_info['TO'] = email_msg['To']
    email_info['DATE'] = email_msg['Date']
    email_info['SUBJECT'] = str(make_header(decode_header(email_msg.get('Subject'))))
     
    if email_msg.is_multipart():
        for part in email_msg.get_payload():
            bytes = part.get_payload(decode=True)
            encode = part.get_content_charset()
            email_info['CONTENT'] = str(bytes, encode)
            email_info['CONTENT'] = clean_email_text(email_info['CONTENT'])
            break
    print(email_info)
    return email_info