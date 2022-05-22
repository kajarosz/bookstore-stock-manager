from flask import jsonify, request
from sqlalchemy.sql import exists
from .models import db, Book
from .google_books import import_books_by_author
from .functions import jsonify_object, query_string_filter, request_to_dict

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
            books_list = imported_books          
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
            filtered_books = query_string_filter(filters)
            books = []
            for book in filtered_books:
                book_details = jsonify_object(book)
                books.append(book_details)
            return jsonify(books)

    @app.route('/books', methods=['POST'])
    def books_post():
        if request.method == 'POST':
            book_dict = request_to_dict(request)
            new_book = Book(**book_dict)
            db.session.add(new_book)
            db.session.commit()
            book_id = new_book._id
            book = Book.query.get(book_id)
            book_details = jsonify_object(book)
            return book_details

    @app.route('/books/<int:_id>', methods=['GET'])
    def get_books_by_id(_id):
        if request.method == 'GET':
            book = Book.query.get(_id)
            book_details = jsonify_object(book)
            return book_details

    @app.route('/books/<int:_id>', methods=['PATCH'])
    def patch_books_by_id(_id):
        if request.method == 'PATCH':
            book = Book.query.get(_id)
            updates = request.json
            db.session.query(Book).filter(Book._id).update(updates)
            db.session.commit()
            book_details = jsonify_object(book)
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


