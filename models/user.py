from pydantic import BaseModel


class User_base(BaseModel):
    username: str = None
    password: str = None

class User(User_base):
    email: str = None
