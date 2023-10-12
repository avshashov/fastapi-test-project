from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import FileResponse

from app.routers import announcements
from app.database.models import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(announcements.router)


@app.get('/', status_code=status.HTTP_200_OK)
async def root() -> FileResponse:
    return FileResponse('app/templates/index.html')
