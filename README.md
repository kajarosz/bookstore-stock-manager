## bookstore-stock-manager

Bookstore Stock Manager is Flask & SQLAlchemy based API designed to import books from Google Books API. Books database can ba managed with standard CRUD operations. App was deployed with Heroku - you can find it [HERE](https://bookstore-stock-manager.herokuapp.com/books)

### How to access endpoints?

Below you will find avaiable methods/endpoints and request body examples.

* POST/import &rarr; Import books from Google Books API by author
```
{
  "author" : "Pratchett"
}
```
* POST/books &rarr; Add single custom book to the database
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


### How to start server?

Fork this repo and clone it to your choosen directory (alternatively you can just download a .zip file and unpack it).
```
git clone https://github.com/kajarosz/bookstore-stock-manager.git
```

Install dependencies - required packages are listed in requirements.txt file. You may need to use pip3 instead of just pip.
```
pip install -r requirements.txt
```

Run run_app.py file in Python. You may need to use python3 instead of just python.
```
python run_app.py
```


### Public APIs used in the project

* *https://developers.google.com/books/docs/v1/using*
