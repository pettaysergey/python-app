from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import engine, Base, SessionDep
from models.books import BookModel
from shemas.books import NewBookSchema

router = APIRouter()


@router.post("/setup_datebase", tags=["Книги"])
async def setup_datebase():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        return {"status": "OK"}


@router.get("/books", tags=["Книги"], summary='Список всем книг')
async def read_books(session: SessionDep) -> list[NewBookSchema]:
    query = select(BookModel)
    elements = await session.execute(query)
    result = elements.scalars().all()

    return result


@router.get("/books/{id}", tags=["Книги"], summary='Получение книги')
async def get_book(id: int, session: SessionDep):
    book = await session.get(BookModel, id)

    if (book):
        return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


@router.put("/books/{id}", tags=["Книги"], summary='Изменение книги')
async def change_book(id: int, session: SessionDep):
    book = await session.get(BookModel, id)

    if (book):
        book.title = 'HELLO!!!!!'
        await session.commit()

        return {"status": '200'}

    raise HTTPException(status_code=404, detail="Книга не найдена")


@router.post('/books', tags=["Книги"], summary="Добавление книги")
async def create_book(data: NewBookSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()

    return {"status": 201}
