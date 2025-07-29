from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# 메일 원본 정보만 저장
class EmailsInfo(BaseModel):
    pk: Optional[int] = None
    uid: str
    from_addr: str
    to_addr: str
    email_date: str
    subject: str
    content: str
    processed_date: datetime
    
    def to_string(self) -> str:
        to_json = self.dict(exclude={"pk", "processed_date"})
        return json.dumps(to_json, ensure_ascii=False)