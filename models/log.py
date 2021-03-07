from pydantic import BaseModel


class create_log(BaseModel):
    request: str = None
    result: dict = None


class log(create_log):
    id: int = None
    owner_id: int = None

    class Config:
        orm_mode = True
