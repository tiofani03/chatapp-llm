from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_name: str
    message: str

class ChatResponse(BaseModel):
    user_name: str
    message: str
    response_time: str
