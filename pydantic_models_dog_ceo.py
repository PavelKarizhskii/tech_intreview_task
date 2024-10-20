from pydantic import BaseModel, ValidationError
from typing import List

# В качестве примера реализована проверка только одной схемы


class GetListSubBreedsResponse(BaseModel):
    message: List[str]
    status: str

