from pydantic import BaseModel
from datetime import  datetime
from typing import Optional

class CreateUser(BaseModel):
    name: str
    fullname: str
    nickname: Optional[str]


class ReadUser(CreateUser):
    id: int
