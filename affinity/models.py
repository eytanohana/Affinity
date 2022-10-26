from pydantic import BaseModel
from datetime import datetime
from typing import Any


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


class FieldValue(BaseModel):
    id: int
    field_id: int
    entity_id: int
    entity_type: int
    list_entry_id: int | None
    value: Any
    value_type: int


class List(BaseModel):
    id: int
    type: int
    name: str
    public: bool
    owner_id: int
    list_size: int


class ListId(List):
    fields: list[Field]


class ListEntry(BaseModel):
    id: int
    list_id: int
    creator_id: int
    entity_type: int
    entity_id: int
    entity: dict
    created_at: datetime

