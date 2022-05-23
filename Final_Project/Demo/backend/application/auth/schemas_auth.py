from pydantic import BaseModel
from typing import Optional

class AuthModel(BaseModel):
    username: str
    email: str
    password: str
    is_editor: Optional[bool]=False

class AuthModelLoging(BaseModel):
    username: str
    password: str
    is_editor: Optional[bool]=False


