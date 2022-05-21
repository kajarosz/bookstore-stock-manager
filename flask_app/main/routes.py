from pkgutil import extend_path
from flask import jsonify, render_template, request,json
from sqlalchemy.sql import exists
from .models import db, Book
from .google_books import import_books_by_author

def configure_routes(app):

    @app.route('/api_spec', methods=['GET'])
    def api_spec():
        response = {"info": {"version": "2022.05.16"}}
        return response

    @app.route('/import', methods=['POST'])
    def import_from_google_api():
        if request.method == 'POST':
            author = request.json['author']
            imported_books = import_books_by_author(author)
            books_list = imported_books[1]          
            books_count = 0
            for book in books_list:
                if not db.session.query(exists().where(Book.external_id == book['external_id'])).scalar():
                    new_book = Book(**book)
                    db.session.add(new_book)
                    db.session.commit()
                    books_count += 1
            response = {"imported": str(books_count)}
            return response
    
   #GET /books?author="Tolkien"&from=2003&to=2022&acquired=false

    @app.route('/books',  methods=['GET'])
    def books_get():
        if request.method == 'GET':
            pass

    @app.route('/books',  methods=['POST'])
    def books_post():
        if request.method == 'POST':
            if request.json['authors']:
                authors = ', '.join(request.json['authors'])
            else:
                authors = None
            book = {'external_id': request.json['external_id'],
                'title': request.json['title'],
                'authors': authors,
                'acquired': request.json['acquired'],
                'published_year': request.json['published_year'],
                'thumbnail': request.json['thumbnail']}
            new_book = Book(**book)
            db.session.add(new_book)
            db.session.commit()
            book_id = new_book._id
            return books_by_id(book_id)


    @app.route('/books/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
    def books_by_id(id):
        book = Book.query.get(id)
        if book.authors:
            authors = book.authors.split(', ')
        else:
            authors = []
        book_json = jsonify({'id': book._id,
                    'external_id': book.external_id,
                    'title': book.title,
                    'authors': authors,
                    'acquired': book.acquired,
                    'published_year': book.published_year,
                    'thumbnail': book.thumbnail
                    })
        return book_json

    #PATCH /books/123

    #DELETE /books/123

