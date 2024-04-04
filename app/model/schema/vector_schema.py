from typing import List
from pydantic import BaseModel

class Vector(BaseModel):
    id: int
    values: List[float]