from flask import jsonify, request
from sqlalchemy.sql import exists
from datetime import date
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
    
    @app.route('/books', methods=['GET'])
    def books_get():
        if request.method == 'GET':
            args = request.args
            filters = args.to_dict()
            keys = filters.keys()
            filtered = Book.query.all()
            if 'author' in keys:
                filtered = list(filter(lambda Book: filters['author'] in str(Book.authors), filtered))
            if 'title' in keys:
                filtered = list(filter(lambda Book: filters['title'] in str(Book.title), filtered))
            if 'acquired' in keys:
                if filters['acquired'] == 'true':
                    filters['acquired'] = True
                else:
                    filters['acquired'] = False
                filtered = list(filter(lambda Book: Book.acquired == filters['acquired'], filtered))
            if 'from' in keys:
                if 'to' in keys:
                    filtered = list(filter(lambda Book: Book.published_year >= filters['from'], filtered))
                    filtered = list(filter(lambda Book: Book.published_year <= filters['to'], filtered))
                else:
                    filtered = list(filter(lambda Book: Book.published_year >= filters['from'], filtered))
            elif 'to' in keys:
                filtered = list(filter(lambda Book: Book.published_year <= filters['to'], filtered))
            print(filtered)
            print(filtered)
            books = []
            for book in filtered:
                if book.authors:
                    authors = book.authors.split(', ')
                else:
                    authors = []
                book_details = {'id': book._id,
                            'external_id': book.external_id,
                            'title': book.title,
                            'authors': authors,
                            'acquired': book.acquired,
                            'published_year': book.published_year,
                            'thumbnail': book.thumbnail
                            }
                books.append(book_details)
            return jsonify(books)

    @app.route('/books', methods=['POST'])
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
            book = Book.query.get(book_id)
            if book.authors:
                authors = book.authors.split(', ')
            else:
                authors = []
            book_details = {'id': book._id,
                        'external_id': book.external_id,
                        'title': book.title,
                        'authors': authors,
                        'acquired': book.acquired,
                        'published_year': book.published_year,
                        'thumbnail': book.thumbnail
                        }
            return book_details

    @app.route('/books/<int:_id>', methods=['GET'])
    def get_books_by_id(_id):
        if request.method == 'GET':
            book = Book.query.get(_id)
            if book.authors:
                authors = book.authors.split(', ')
            else:
                authors = []
            book_details = {'id': book._id,
                        'external_id': book.external_id,
                        'title': book.title,
                        'authors': authors,
                        'acquired': book.acquired,
                        'published_year': book.published_year,
                        'thumbnail': book.thumbnail
                        }
            return book_details

    @app.route('/books/<int:_id>', methods=['PATCH'])
    def patch_books_by_id(_id):
        if request.method == 'PATCH':
            book = Book.query.get(_id)
            updates = request.json
            db.session.query(Book).filter(Book._id).update(updates)
            db.session.commit()
            if book.authors:
                authors = book.authors.split(', ')
            else:
                authors = []
            book_details = {'id': book._id,
                        'external_id': book.external_id,
                        'title': book.title,
                        'authors': authors,
                        'acquired': book.acquired,
                        'published_year': book.published_year,
                        'thumbnail': book.thumbnail
                        }
            return book_details

    @app.route('/books/<int:_id>', methods=['DELETE'])
    def delete_books_by_id(_id):
        if request.method == 'DELETE':
            book = Book.query.get(_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                response = {'info': 'Book deleted'}
            else:
                response = {'info': 'This book is not stored in database'}
            return response


