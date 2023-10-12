from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.database import models
from app import schemas


async def get_announcement(session: AsyncSession, id: int) -> models.Announcement | None:
    result = await session.execute(select(models.Announcement).where(models.Announcement.id == id))
    return result.scalar()


async def get_announcements(session: AsyncSession) -> list[models.Announcement]:
    result = await session.scalars(select(models.Announcement).order_by(models.Announcement.id))
    return list(result.all())


async def create_announcement(session: AsyncSession, data: schemas.AnnouncementCreate) -> models.Announcement:
    announcement = models.Announcement(**data.model_dump())
    session.add(announcement)
    await session.commit()
    return announcement


async def delete_announcement(session: AsyncSession, id: int) -> None:
    await session.execute(delete(models.Announcement).where(models.Announcement.id == id))
    await session.commit()


async def update_announcement(session: AsyncSession,
                              id: int,
                              data: schemas.AnnouncementCreate) -> models.Announcement:
    update_query = (update(models.Announcement).
                    where(models.Announcement.id == id).
                    values(**data.model_dump()).returning(models.Announcement))

    announcement = await session.execute(update_query)
    await session.commit()
    return announcement.scalar()
