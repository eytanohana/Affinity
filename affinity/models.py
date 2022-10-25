from pydantic import BaseModel


class List(BaseModel):
    id: int
    type: int
    name: str
    public: bool
    owner_id: int
    list_size: int
