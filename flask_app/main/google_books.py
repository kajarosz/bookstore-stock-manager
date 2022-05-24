import requests, math
from .exceptions import ApiRequestException

# Google Books API UR address with string query to request for books by given author
google_books_api = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:'
# maximum results number per request (API limitation)
max_results = 40
# string query to define number of results per request
end_index = f'&maxResults={max_results}'


# Importing books from Google Books API
# Split request into batches because of responses limit
# Use custom functions request_book_details() and extract_book_details()
def import_books_by_author(author):
    # Request first batch (index 0)
    response = request_books_details(author)
    # Get number of books by given author
    try:
        total_items = response.get('totalItems')
    except:
        message = 'Error occured while creating request batches.'
        raise ApiRequestException(message)
    # If there are no books, return None
    if total_items == 0:
        return None
    # If there are books by given author...
    else:
        # ... calculate number of needed batches...
        no_of_requests = math.ceil(total_items / max_results)
        books = []
        # ... and extract books details for first batch...
        books_batch = extract_books_details(response)
        books.extend(books_batch)
        # ... and request and extract books details for rest of the batches.
        for i in range (no_of_requests):
            if i != 0:
                start_index = f'&startIndex={i*max_results}'
                response = request_books_details(author, start_index)
                books_batch = extract_books_details(response)
        return books

# Importing books from Google Books API
# Request data
def request_books_details(author, start_index='&startIndex=0'):
    # Create request URL
    url = google_books_api + author + start_index + end_index
    # Request data
    try:
        response = requests.get(url).json()
    except:
        message = 'Unknown Google Books API error.'
        raise ApiRequestException(message)
    return response

# Importing books from Google Books API
# Extract data
def extract_books_details(response):
    # Check is items exist in API response
    try:
        items = response.get('items')
    except:
        message = 'No items were found.'
        raise ApiRequestException(message)
    books_batch = []
    for item in items:
        # get and process books details
        try:
            external_id = item.get('id')
            details = item.get('volumeInfo')
            title = details.get('title')
            if details.get('authors'):
                authors = ', '.join(details.get('authors'))
            else:
                authors = None
            acquired = False
            if details.get('publishedDate'):
                published_year = details.get('publishedDate')[:4]
            else:
                published_year = None
        except:
            message = 'Error occured while collecting item data.'
            raise ApiRequestException(message)
        thumbnail = f'http://books.google.com/books/content?id={external_id}&printsec=frontcover&img=1&zoom=1&source=gbs_api%22'
        # create book details dictionary
        book = {'external_id': external_id,
        'title': title,
        'authors': authors,
        'acquired': acquired,
        'published_year': published_year,
        'thumbnail': thumbnail
        }
        books_batch.append(book)
    return books_batch