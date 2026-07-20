from pydantic import BaseModel

class Repository(BaseModel):

    name: str
    description: str
    language: str
    stars: int
    owner: str


