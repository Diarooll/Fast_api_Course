from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'a volta dos que nao foram', 'author': 'autor 1', 'category': 'acao'},
    {'title': 'cocozao mole', 'author': 'autor 2', 'category': 'romance'},
    {'title': 'a ida dos que nao vao', 'author': 'autor 3', 'category': 'acao'},
    {'title': 'popote mole', 'author': 'autor 1', 'category': 'acao'},

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


@app.get('/books/')
async def read_category_by_query(category: str):
    return [book for book in BOOKS if book.get('category').casefold() == category.casefold()]


@app.get('/books/author/{author}')
async def search_by_author(author: str):
    return [book for book in BOOKS if book.get('author').casefold() == author.casefold()]


@app.get('/books/author/{author}/')
async def read_author_category_by_query(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and \
        book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return    



#post method
@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

#put method
@app.put('/books/update_book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete('/books/delete_book/{book_title}')
async def delete_book_title(book_title):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break