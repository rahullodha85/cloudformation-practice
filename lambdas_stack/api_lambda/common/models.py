from pydantic import BaseModel


class MessageIn(BaseModel):
    message: str
