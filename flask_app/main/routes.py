from flask import jsonify, render_template, request,json
from sqlalchemy.sql import exists
from .models import db, Book
from .google_books import import_books_by_author

def configure_routes(app):

    @app.route('/import', methods=['POST'])
    def import_books():
        if request.method == 'POST':
            author = request.json['author']
            imported_books = import_books_by_author(author)
            books_list = imported_books[1]
            #external_id_set = set(Book.query.with_entities(Book.external_id).all())
            
            books_count = 0
            for book in books_list:
                if not db.session.query(exists().where(Book.external_id == book['external_id'])).scalar():
                    new_book = Book(**book)
                    db.session.add(new_book)
                    db.session.commit()
                    books_count += 1
            #books_count = imported_books[0]
            response = {"imported": str(books_count)}
            return response

    @app.route('/home')
    def home():
        return 'hello!'