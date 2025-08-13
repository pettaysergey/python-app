from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel, Field, ConfigDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///books.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str]
    title: Mapped[str]


class NewBook(BaseModel):
    author: str = Field(max_length=100)
    title: str = Field(max_length=100)
    id: int

    model_config = ConfigDict(extra='forbid')


@app.post("/setup_datebase", tags=["Книги"])
async def setup_datebase():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        return {"status": "OK"}


@app.get("/books", tags=["Книги"], summary='Список всем книг')
async def read_books(session: SessionDep) -> list[NewBook]:
    query = select(BookModel)
    elements = await session.execute(query)
    result = elements.scalars().all()

    return result


@app.get("/books/{id}", tags=["Книги"], summary='Получение книги')
async def get_book(id: int, session: SessionDep):
    query = select(BookModel)
    elements = await session.execute(query)
    result = elements.scalars().all()

    for book in result:
        print(book)
        if (book.id == id):
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.post('/books', tags=["Книги"], summary="Добавление книги")
async def create_book(data: NewBook, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()

    return {"status": 201}


if __name__ == ("__main__"):
    uvicorn.run("main:app", host='127.0.0.1', port=8127, reload=True)
