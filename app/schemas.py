from datetime import datetime

from pydantic import BaseModel


class AnnouncementBase(BaseModel):
    title: str
    description: str
    owner_id: int


class AnnouncementCreate(AnnouncementBase):
    pass


class Announcement(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
