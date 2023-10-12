from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import models
from app.database import announcements as crud

router = APIRouter(prefix='/announcements', tags=['announcements'])

SessionLocal = Annotated[AsyncSession, Depends(models.get_session)]


@router.get('/', response_model=list[schemas.Announcement])
async def get_all_announcements(db: SessionLocal):
    announcements = await crud.get_announcements(db)
    return announcements


@router.get('/{id}', response_model=schemas.Announcement)
async def get_announcement(db: SessionLocal, id: int):
    announcement = await crud.get_announcement(db, id)
    return announcement


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Announcement)
async def create_announcement(db: SessionLocal, announcement: schemas.AnnouncementCreate):
    result = await crud.create_announcement(db, announcement)
    return result


@router.delete('/{id}')
async def delete_announcement(db: SessionLocal, id: int):
    await crud.delete_announcement(db, id)


@router.put('/{id}', response_model=schemas.Announcement)
async def full_update_announcement(db: SessionLocal,
                                   id: int,
                                   data: schemas.AnnouncementCreate):
    announcement = await crud.get_announcement(db, id)
    if announcement:
        result = await crud.update_announcement(db, id, data)
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Announcement not found')


@router.patch('/{id}')
async def part_update_announcement():
    pass
