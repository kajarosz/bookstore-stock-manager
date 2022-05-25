## bookstore-stock-manager

Bookstore Stock Manager is Flask & SQLAlchemy based REST API designed to import books from Google Books API. Books database can ba managed with standard CRUD operations. API accepts and returns data in JSON format. App was deployed with Heroku - you can find it [HERE](https://bookstore-stock-manager.herokuapp.com/books).


### How to access endpoints?

Below you will find avaiable methods/endpoints and request body examples.

* __POST/import__ &rarr; Import books from Google Books API by author. If book already exists in database (it's veryfied based on Google Books book ID), data will be updated.
```
{
  "author" : "Pratchett"
}
```
* __POST/books__ &rarr; Add single custom book to the database
```
{
  "acquired": true,
  "authors": [
      "Karolina Jarosz"
  ],
  "external_id": null,
  "published_year": "2022",
  "thumbnail": null,
  "title": "How to manage your book store?"
 }
 ```
* __GET/api_spec__ &rarr; Basic info about API
* __GET/books?author=Karolina&title=store%from=2003&to=2022&acquired=true__ &rarr; Get books info filtered by author, title, published year tange and acquired status. If no filters are given, API will return list of all books.
* __GET/books/1__ &rarr; Get single book info for given ID
* __DEL/books/1__ &rarr; Delete book for given ID
* __PATCH/books/1__ &rarr; Update book info for given ID
```
{
  "acquired" : false
}
```


### How to start server locally in development mode?

1. Fork this repo and clone it to your choosen directory (alternatively you can just download a .zip file and unpack it).
```
git clone https://github.com/kajarosz/bookstore-stock-manager.git
```

2. Install dependencies - required packages are listed in requirements.txt file. You may need to use pip3 instead of just pip.
```
pip install -r requirements.txt
```

3. Inside run_app.py file: set enviroment to development mode & paste your database URI:
```
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/bookstore'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
```

4. Run run_app.py file in Python. You may need to use python3 instead of just python.
```
python run_app.py
```


### How to run tests?

In project directory run:
```
pytest
```

### Public APIs used in the project

*https://developers.google.com/books/docs/v1/using*
