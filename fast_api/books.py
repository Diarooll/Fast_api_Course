from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'a volta dos que nao foram', 'gender': 'acao'},
    {'title': 'cocozao mole', 'gender': 'romance'},
    {'title': 'a ida dos que nao vao', 'gender': 'acao'}
]


@app.get('/')
async def pagina_inicial():
    return {'message': 'Essa é a pagina principal'}

@app.get('/books')
async def show_all_books():
    return BOOKS


@app.get('/books/mybook')
async def my_favorite_book():
    return {'Book title': 'a caida dos que cairam'}


@app.get('/books/{book_title}')
async def search_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'Error': 'inexisting book'}