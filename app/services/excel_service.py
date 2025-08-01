import os
from openpyxl import Workbook
from datetime import datetime

# GPT 응답 데이터 작성

sheet_name = os.getenv("SHEET_NAME")
excel_path = os.getenv("EXCEL_PATH").format(datetime.now().strftime("%Y%m%d_%H%M"))

def write_data(gpt_list):
    excel = Workbook()
    sheet = excel.active
    sheet.title = sheet_name
    
    # Key값 1행에 작성
    headers = list(gpt_list[0].keys())
    sheet.append(headers)
    
    # Value값 2행부터 작성
    for item in gpt_list:
        if item['is_subscription']:
            row = [item[key] for key in headers]
            sheet.append(row)
    
    excel.save(excel_path)
    return excel_path