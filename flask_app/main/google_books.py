import requests, math

class ApiRequestException(Exception):
    pass

google_books_api = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:'
max_results = 40
no_of_requests = f'&maxResults={max_results}'

def import_books_by_author(author):
    response = request_books_details(author)
    total_items = response.get('totalItems')
    no_of_requests = math.ceil(total_items / max_results)
    books = []
    for i in range (no_of_requests):
        if i != 0:
            start_index = f'&startIndex={i*max_results}'
            response = request_books_details(author, start_index)
        books_batch = extract_books_details(response)
        books.extend(books_batch)
    return books

def request_books_details(author, start_index='&startIndex=0'):
    url = google_books_api + author + start_index + no_of_requests
    try:
        response = requests.get(url).json()
    except ApiRequestException:
        response = {'info': 'Unknown Google Books API error.'}
    return response
    
def extract_books_details(response):
    items = response.get('items')
    books_batch = []
    for item in items:
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
        thumbnail = f'http://books.google.com/books/content?id={external_id}&printsec=frontcover&img=1&zoom=1&source=gbs_api%22'
        book = {'external_id': external_id,
        'title': title,
        'authors': authors,
        'acquired': acquired,
        'published_year': published_year,
        'thumbnail': thumbnail
        }
        books_batch.append(book)
    return books_batch