from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

import services
from models import ShowText, TextObjectCreate

# create engine for interaction with database
engine = create_engine('postgresql+asyncpg://mac:postgres@0.0.0.0:5432/postgres', future=True, echo=True)

# create session for the interaction with database
async_sessions = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

app = FastAPI(title="text_project")


class TextMode:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_text(self, text: str, salt: str):
        new_text = TextObjectCreate(
            text=text,
            salt=salt
        )
        self.db_session.add(new_text)
        await self.db_session.flush()
        return new_text


@app.get("/", response_model=None)
def read_root():
    return {"Hello": "World"}


async def create_new_text(body: TextObjectCreate):
    async with async_session() as session:
        async with session.begin():
            text_mode = TextMode(session)
            text = await text_mode.create_text(
                text=body.text,
                salt=""

            )

            return ShowText(
                text=text.text,
                salt=services.get_salt()
            )


@app.post("/", response_model=ShowText)
async def create_text(text: TextObjectCreate) -> ShowText:
    salt = services.get_salt()
    hash_with_salt = services.hash_with_salt(salt, text.text)
    return hash_with_salt
