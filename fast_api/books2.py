from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookModel(BaseModel):
    id: Optional[int] = Field(description="id is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(max_length=100)
    rating: int = Field(ge=0, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithdiego",
                "description": "a new description for a book",
                "rating": 5
            }
        }
    }



BOOKS = [
        Book(1, 'computer science pro', 'codingwithroby', 'a very nice book', 4),
        Book(2, 'getting better at FastAPI', 'codingwithroby', 'a nice book', 5),
        Book(3, 'Software', 'diego', 'a great book', 3)

]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create_book")
async def create_book(book_request: BookModel): #passa o modelo do BookModel como obrigatorio
    new_book = Book(**book_request.model_dump()) #pega a dict do book_request q é oq é passado no request
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
