import datetime
from typing import Optional

from pydantic import BaseModel


class Vid(BaseModel):
    vid: int


class RefHash(BaseModel):
    ref_hash: str


class Ref(BaseModel):
    ref: str


class Id(BaseModel):
    id: int


class RecordCreator(BaseModel):
    ref: str
    content: dict


class Record(BaseModel):
    ref_hash: str
    vid: int
    content: dict
    evolution: dict

    created_at: datetime.datetime


class RegisterRefResponse(BaseModel):
    id: int
    ref: str
    ref_hash: str


class VersionResponse(BaseModel):
    id: Optional[int]
    vid: Optional[int]
    ref: Optional[str]
    ref_hash: Optional[str]
    content: Optional[dict]
    evolution: Optional[dict]
    content_hash: Optional[str]
    exists: Optional[bool] = True


class NotifyUserResponse(BaseModel):
    version: VersionResponse
    user: str
    message: Optional[dict]
    is_notified: bool


class MergeEvolution(VersionResponse):
    old_vid: Optional[int]
    new_vid: Optional[int]
    error: Optional[str] = None


