from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    _id = db.Column('id', db.Integer, primary_key = True)
    external_id = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(500), unique=False)
    authors = db.Column(db.String(500), unique=False)
    acquired = db.Column(db.Boolean, unique=False)
    published_year = db.Column(db.String(500), unique=False)
    thumbnail = db.Column(db.String(500), unique=False)

    def __str__(self):
        return f'{self.title} by {self.authors}'