from pydantic import BaseModel

class MessageRequest(BaseModel):
    user_id: str
    thread_id: str
    text: str

class MessageResponse(BaseModel):
    messages: list
    language: str
