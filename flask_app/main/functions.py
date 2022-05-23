from .models import Book
from .exceptions import FunctionException

# JSONify book object
def jsonify_object(book):
    try:
        # Split authors string into list
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
    except:
        message = 'Error occured while parsing object into JSON format.'
        raise FunctionException(message)
    return book_details

# Process request into dictionary
def request_to_dict(request):
    try:
        # Split authors string into list
        if request.json['authors']:
            authors = ', '.join(request.json['authors'])
        else:
            authors = None
        book_dict = request.json
        book_dict.update({'authors': authors})
    except:
        message = 'Error occured while parsing request into JSON format.'
        raise FunctionException(message)
    return book_dict

# Filter all books query by string query arguments
def query_string_filter(filters):
    # get filter keys
    keys = filters.keys()
    # query all books
    try:
        filtered_books = Book.query.all()
    except:
        message = 'Error occured while querying book list from database.'
        raise FunctionException(message)
    try:
        # filter by author
        if 'author' in keys:
            filtered_books = list(filter(lambda Book: filters['author'] in str(Book.authors), filtered_books))
        # filter by title
        if 'title' in keys:
            filtered_books = list(filter(lambda Book: filters['title'] in str(Book.title), filtered_books))
        # filter by acquired status
        if 'acquired' in keys:
            if filters['acquired'] == 'true':
                filters['acquired'] = True
            else:
                filters['acquired'] = False
            filtered_books = list(filter(lambda Book: Book.acquired == filters['acquired'], filtered_books))
        # filter by published date
        if 'from' in keys:
            if 'to' in keys:
                filtered_books = list(filter(lambda Book: Book.published_year >= filters['from'], filtered_books))
                filtered_books = list(filter(lambda Book: Book.published_year <= filters['to'], filtered_books))
            else:
                filtered_books = list(filter(lambda Book: Book.published_year >= filters['from'], filtered_books))
        elif 'to' in keys:
            filtered_books = list(filter(lambda Book: Book.published_year <= filters['to'], filtered_books))
    except:
        message = 'Error occured while filtering data.'
        raise FunctionException(message)
    return filtered_books