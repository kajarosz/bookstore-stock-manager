from types import NoneType
from flask_app.main.google_books import import_books_by_author, request_books_details, extract_books_details
from flask_app.main.exceptions import ApiRequestException
from .mockup_variables import author_valid, author_invalid, start_index_invalid, json_input_valid, json_input_invalid
import pytest

def test_request_book_details_valid():
     response = request_books_details(author_valid)
     assert isinstance(response, dict)
     assert 'kind' in response

def test_request_book_details_invalid():
     with pytest.raises(ApiRequestException):
        response = request_books_details(author_valid, start_index_invalid)

def test_extract_book_details_valid():
    response = extract_books_details(json_input_valid)
    assert isinstance(response, list)
    assert isinstance(response[0], dict)

def test_extract_book_details_invalid():
    with pytest.raises(ApiRequestException):
        response = extract_books_details(json_input_invalid)

def test_import_books_by_author_valid():
    response = import_books_by_author(author_valid)
    assert isinstance(response, list)

def test_import_books_by_author_invalid():
    response = import_books_by_author(author_invalid)
    assert isinstance(response, NoneType)
