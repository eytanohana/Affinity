from pydantic import BaseModel


class DropdownOption(BaseModel):
    id: int
    color: int
    rank: int
    text: str


class Field(BaseModel):
    id: int
    name: str
    list_id: int
    allows_multiple: bool
    dropdown_options: list[DropdownOption]
    value_type: int
    track_changes: bool
    enrichment_source: str


class List(BaseModel):
    id: int
    type: int
    name: str
    public: bool
    owner_id: int
    list_size: int


class ListId(List):
    fields: list[Field]


