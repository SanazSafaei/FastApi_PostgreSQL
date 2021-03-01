from pydantic import BaseModel


class User_base(BaseModel):
    username: str = None
    email: str = None

class User(User_base):
    password: str = None
