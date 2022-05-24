from flask import Flask
from main.routes import configure_routes
from main.models import db

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/bookstore'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oukvzjqvabqlsx:a29a655a62c206124df42ba5b60fb0f01266bec2c7b197f5d528e348633f2756@ec2-3-231-82-226.compute-1.amazonaws.com:5432/d31j0200983ajp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_routes(app)

if __name__ == '__main__':
    #if ENV == 'dev':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()