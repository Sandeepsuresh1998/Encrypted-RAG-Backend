from pydantic import BaseModel

class EmbeddingCreate(BaseModel):
    user_id: str
    text: str
