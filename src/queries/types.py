from pydantic import BaseModel

class QueryGenerate(BaseModel):
    user_id: str
    text: str
