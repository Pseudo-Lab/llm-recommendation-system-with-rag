import uuid
from typing import List
from pydantic import BaseModel

class Vector(BaseModel):
    id: int
    values: List[float]

class Gen(BaseModel):
    workspace_id: uuid.UUID
    input: str

class Search(BaseModel):
    workspace_id: uuid.UUID
    input: str
    top_k: int

    class Config:
        json_schema_extra = {
            "example": {
                "workspace_id": "76241726-616d-46bd-81ff-dfd07579d069",
                "input": "show me the korean movies?",
                "top_k": 2
            }
        }


