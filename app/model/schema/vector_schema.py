import uuid
from typing import List
from pydantic import BaseModel

class Vector(BaseModel):
    id: int
    values: List[float]

class Gen(BaseModel):
    workspace_id: uuid.UUID
    input: str

class SimilaritySearch(BaseModel):
    workspace_id: uuid.UUID
    input: str
