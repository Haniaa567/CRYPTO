from pydantic import BaseModel
from typing import Optional


class TestModel(BaseModel):
    a: str
    b: Optional[int]

schema = TestModel.model_json_schema()
print(schema)