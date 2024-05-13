from pydantic import BaseModel

from .chat import Chat


class ChatUpdate(BaseModel):
    chat: Chat
    action: str
    object_guid: str
