from pydantic import BaseModel, Field, ConfigDict


class NewBookSchema(BaseModel):
    author: str = Field(max_length=100)
    title: str = Field(max_length=100)
    id: int

    model_config = ConfigDict(extra='forbid')
