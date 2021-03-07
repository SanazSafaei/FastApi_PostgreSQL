from pydantic import BaseModel
from typing import List

from models.log import log


class User_base(BaseModel):
    username: str = None
    email: str = None
    is_active: bool = False


class User_create(User_base):
    password: str = None


class User(User_base):
    id: int = None
    logs: List[log] = []

    class Config:
        orm_mode = True
