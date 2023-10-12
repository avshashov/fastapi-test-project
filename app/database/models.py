from datetime import datetime

from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DSN = 'sqlite+aiosqlite:///app/database/database.db'
engine = create_async_engine(DSN, echo=True)
async_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class Announcement(Base):
    __tablename__ = 'announcement'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey('author.id'))

    owner: Mapped['Author'] = relationship(back_populates='announcements')


class Author(Base):
    __tablename__ = 'author'

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(unique=True, nullable=False)

    announcements: Mapped[list['Announcement'] | None] = relationship(back_populates='owner')
