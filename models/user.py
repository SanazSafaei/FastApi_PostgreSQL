from pydantic import BaseModel


class User_base(BaseModel):
    username: str = None
    Password: str = None

class User(User_base):
    Email: str = None
