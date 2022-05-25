from flask import jsonify, request
from sqlalchemy.sql import exists
from .models import db, Book
from .google_books import import_books_by_author
from .functions import jsonify_object, query_string_filter, request_to_dict
from .exceptions import GeneralException, RoutingException


def configure_routes(app):

    # Error handler for custom excaptons
    @app.errorhandler(GeneralException)
    def exception_raised(e):
        return jsonify(e.message), e.status_code

    # Error handler for 404: resource not found
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404
    
    # Error handler for 405: method not allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error=str(e)), 405

    # getting the info about API
    @app.route('/api_spec', methods=['GET'])
    def api_spec():
        response = {"info": {"version": "2022.05.16"}}
        return response

    # import books
    # Download data about books from
    # https://www.googleapis.com/books/v1/volumes
    # for requested author.
    # Add new entries into the application database.
    # Update already existing ones.
    @app.route('/import', methods=['POST'])
    def import_from_google_api():
        if request.method == 'POST':
            author = request.json['author']
            # import books by given author
            imported_books = import_books_by_author(author)
            # create imported books counter
            imported_books_count = 0
            if imported_books:     
                    for book in imported_books:
                        # based on external ID, check if book exists in database
                        # if no: add new book
                        if not db.session.query(exists().where(Book.external_id == book['external_id'])).scalar():
                            try:
                                new_book = Book(**book)
                                db.session.add(new_book)
                                db.session.commit()
                                imported_books_count += 1
                            except:
                                message = 'Error occured while adding book to database.'
                                raise RoutingException(message)
                        # if yes: update book details 
                        else:
                            try:
                                # remove external_id key-value pair for dict
                                # because it is existing unique value
                                external_id = book['external_id']
                                book.pop('external_id')
                                # update book details
                                db.session.query(Book).filter(Book.external_id == external_id).update(book)
                                db.session.commit()
                                imported_books_count += 1
                            except:
                                message = 'Error occured while updating book in database.'
                                raise RoutingException(message)
            response = {'imported': str(imported_books_count)}
            return response
    
    # getting the list of books from the database
    @app.route('/books', methods=['GET'])
    def books_get():
        if request.method == 'GET':
            # get string query arguments
            try:
                args = request.args
                filters = args.to_dict()
            except:
                message = 'Error occured while accessing query string arguments.'
                raise RoutingException(message)
            # filter books
            filtered_books = query_string_filter(filters)
            books = []
            # JSONify filtered books details
            for book in filtered_books:
                book_details = jsonify_object(book)
                books.append(book_details)
            return jsonify(books)

    # get details of single book
    @app.route('/books/<int:_id>', methods=['GET'])
    def get_books_by_id(_id):
        if request.method == 'GET':
            # get book object by ID
            book = Book.query.get(_id)
            # if book exists, JSONify details and return
            if book:
                book_details = jsonify_object(book)
                return book_details
            # if book does not exist, return message
            else:
                response = {'info': 'This book is not in the database.'}
                return response

    # add a new book to collection
    @app.route('/books', methods=['POST'])
    def books_post():
        if request.method == 'POST':
            # process request into dictionary
            print(type(request))
            print(request)
            book_dict = request_to_dict(request)
            # create new book object and add to database
            new_book = Book(**book_dict)
            db.session.add(new_book)
            db.session.commit()
            # get new book details and return
            book_id = new_book._id
            book = Book.query.get(book_id)
            book_details = jsonify_object(book)
            return book_details
            
    # update details of single book
    @app.route('/books/<int:_id>', methods=['PATCH'])
    def patch_books_by_id(_id):
        if request.method == 'PATCH':
            # get requested book object
            book = Book.query.get(_id)
            # JSONify request details
            updates = request.json
            # update book details
            db.session.query(Book).filter(Book._id == _id).update(updates)
            db.session.commit()
            book_details = jsonify_object(book)
            return book_details

    # delete a book
    @app.route('/books/<int:_id>', methods=['DELETE'])
    def delete_books_by_id(_id):
        if request.method == 'DELETE':
            # get requested book object
            book = Book.query.get(_id)
            # if book exists, delete it
            if book:
                db.session.delete(book)
                db.session.commit()
                response = {'info': 'Book deleted'}
            # if book does not exist, return message
            else:
                response = {'info': 'This book is not in the database.'}
            return response