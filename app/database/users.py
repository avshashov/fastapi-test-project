from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models


async def author_exists(session: AsyncSession, id: int) -> bool:
    user = await session.execute(select(models.Author).where(models.Author.id == id))
    return bool(user.first())
