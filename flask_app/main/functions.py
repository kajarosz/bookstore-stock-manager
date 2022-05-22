from .models import Book

def jsonify_object(book):
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

def request_to_dict(request):
    if request.json['authors']:
        authors = ', '.join(request.json['authors'])
    else:
        authors = None
    book_dict = {'external_id': request.json['external_id'],
        'title': request.json['title'],
        'authors': authors,
        'acquired': request.json['acquired'],
        'published_year': request.json['published_year'],
        'thumbnail': request.json['thumbnail']}
    return book_dict

def query_string_filter(filters):
    keys = filters.keys()
    filtered_books = Book.query.all()
    if 'author' in keys:
        filtered_books = list(filter(lambda Book: filters['author'] in str(Book.authors), filtered_books))
    if 'title' in keys:
        filtered_books = list(filter(lambda Book: filters['title'] in str(Book.title), filtered_books))
    if 'acquired' in keys:
        if filters['acquired'] == 'true':
            filters['acquired'] = True
        else:
            filters['acquired'] = False
        filtered_books = list(filter(lambda Book: Book.acquired == filters['acquired'], filtered_books))
    if 'from' in keys:
        if 'to' in keys:
            filtered_books = list(filter(lambda Book: Book.published_year >= filters['from'], filtered_books))
            filtered_books = list(filter(lambda Book: Book.published_year <= filters['to'], filtered_books))
        else:
            filtered_books = list(filter(lambda Book: Book.published_year >= filters['from'], filtered_books))
    elif 'to' in keys:
        filtered_books = list(filter(lambda Book: Book.published_year <= filters['to'], filtered_books))
    return filtered_books