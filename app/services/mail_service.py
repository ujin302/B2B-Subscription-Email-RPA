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
def getEmailList():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)

    imap.select("INBOX")
    #받은 편지함 모든 메일 검색
    status, data = imap.uid('search', None, 'ALL')

    allEmail = data[0].split()
    allEmail.reverse()
    allEmailInfo = []
    
    for mail in allEmail:
        allEmailInfo.append(getEmailInfo(mail, imap))
    
    imap.close()
    imap.logout()
    return allEmailInfo

# 메일 정보 추출
def getEmailInfo(mail, imap):
    emailInfo = {} # 메일 정보 저장
    
    result, data = imap.uid('fetch', mail, '(RFC822)')
    rawEmail = data[0][1]
    emailMSG = email.message_from_bytes(rawEmail)
    
    # 메일 정보
    emailInfo['FROM'] = str(make_header(decode_header(emailMSG.get('From'))))
    emailInfo['SENDER'] = emailMSG['Sender']
    emailInfo['TO'] = emailMSG['To']
    emailInfo['DATE'] = emailMSG['Date']
    emailInfo['SUBJECT'] = str(make_header(decode_header(emailMSG.get('Subject'))))
     
    if emailMSG.is_multipart():
        for part in emailMSG.get_payload():
            bytes = part.get_payload(decode=True)
            encode = part.get_content_charset()
            emailInfo['CONTENT'] = str(bytes, encode)
            emailInfo['CONTENT'] = clean_email_text(emailInfo['CONTENT'])

            break
    print(emailInfo)
    return emailInfo