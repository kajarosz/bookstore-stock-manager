#from run_app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    _id = db.Column('id', db.Integer, primary_key = True)
    external_id = db.Column(db.String(12), unique=True)
    title = db.Column(db.String(500), unique=False)
    authors = db.Column(db.String(500), unique=False)
    aquired = db.Column(db.Boolean, unique=False)
    published_year = db.Column(db.String(500), unique=False)
    thumbnail = db.Column(db.String(500), unique=False)