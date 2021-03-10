import pytest
from rag.validation import ValidationError, reject
from rag.validation.converters.integer import integer
from rag.validation.converters.string import string
from rag.validation.converters.boolean import boolean
from rag.validation.converters.model import model


def test_integer():
    assert integer("123") == 123
    assert integer(123) == 123

def test_string():
    assert string(123) == "123"
    assert string("123") == "123"

def test_boolean():
    assert boolean(0) == False
    assert boolean(1) == True
    assert boolean("false") == False
    assert boolean("true") == True
    assert boolean("False") == False
    assert boolean("True") == True
