from flask import Flask
from main.routes import configure_routes
from main.models import db

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/bookstore'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_routes(app)

db.init_app(app)

if __name__ == '__main__':
    app.run()