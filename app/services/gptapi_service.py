import os
from openai import OpenAI

gpt_api_key = os.getenv("GPT_API_KEY")
system_content = """
    너는 통신사 B2B 청약 관리자야.
    내가 메일 정보를 제공하면 너는 필요한 청약 데이터를 json 형태로 추출할 수 있어.
    하지만, 너에게 제공하는 모든 메일이 청약 메일이 아니고 청약과 관련 없는 메일이 있을 수도 있어.
    
    내가 제공하는 데이터를 잘 판단해서 반드시 아래 JSON 스키마에 따라 대답해줘.
    {
        "is_subscription": true/false, 
        "company_name": string or null,
        "contact_name": string or null,
        "phone": string or null,
        "email": string or null,
        "service_name": string or null,
        "quantity": int or null,
        "installation_date": string (YYYY-MM-DD) or null,
        "address": string or null,
        "contract_type": string or null,
        "additional_request": string or null
    }
    
    그리고 이건 내가 너에게 제공할 메일 정보 데이터의 형식이야. 참고해줘
    {
        "UID":  ,
        "FROM":  ,
        "SENDER":  ,
        "TO":  ,
        "DATE":  ,
        "SUBJECT":  ,
        "CONTENT":
    }
"""

# 청약 데이터 추출
def ask_gpt(mail_list):
    client = OpenAI(api_key=gpt_api_key)
    gpt_list = []
    for mail_info in mail_list:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": mail_info}
            ],
            max_tokens=500
        )
        
        gpt_list.append(response.choices[0].message['content'])
        
    return  gpt_list