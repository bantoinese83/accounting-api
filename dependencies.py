from contextlib import asynccontextmanager
from sqlmodel import Session, SQLModel
from config import engine


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app):
    SQLModel.metadata.create_all(engine)
    print("Database Initialized.")
    yield


