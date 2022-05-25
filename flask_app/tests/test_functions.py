from flask_app.main.functions import jsonify_object, request_to_dict, query_string_filter
from flask_app.main.exceptions import FunctionException
from .mockup_variables import request_valid, request_invalid, book_valid, book_invalid, filters_valid, filters_invalid
import pytest


def test_jsonify_object_valid():
    response = jsonify_object(book_valid)
    assert isinstance(response, dict)
    assert isinstance(response['authors'], list)

def test_jsonify_object_invalid():
    with pytest.raises(FunctionException):
        response = jsonify_object(book_invalid)

def test_request_to_dict_valid():
    response = request_to_dict(request_valid)
    assert isinstance(response, dict)
    assert isinstance(response['authors'], str)

def test_request_to_dict_invalid():
    with pytest.raises(FunctionException):
        response = request_to_dict(request_invalid)

#def test_query_string_filter_valid():
    #response = query_string_filter(filters_valid)
    #assert isinstance(response, list)

def test_query_string_filter_invalid():
    with pytest.raises(FunctionException):
        response = query_string_filter(filters_invalid)

