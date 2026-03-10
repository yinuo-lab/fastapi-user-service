from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

from app.models.user import User  # noqa: F401
from app.api.routers.auth import router as auth_router
from app.api.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown（目前不用写）


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/ping")
def ping():
    return {"msg": "ok"}