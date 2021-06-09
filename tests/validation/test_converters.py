import pytest
from decimal import Decimal
from rag.validation import ValidationError, reject
from rag.validation.converters.boolean import boolean
from rag.validation.converters.decimal import decimal
from rag.validation.converters.floating import floating
from rag.validation.converters.integer import integer
from rag.validation.converters.json import json
from rag.validation.converters.model import model
from rag.validation.converters.models import models
from rag.validation.converters.number import number
from rag.validation.converters.string import string


def test_boolean():
    assert boolean(0) == False
    assert boolean(1) == True
    assert boolean("false") == False
    assert boolean("true") == True
    assert boolean("False") == False
    assert boolean("True") == True

def test_decimal():
    assert decimal('1') == Decimal('1')
    assert decimal('1.2') == Decimal('1.2')
    assert decimal('123') == Decimal('123')
    assert decimal(123) == Decimal('123')

def test_floating():
    assert floating("123") == 123
    assert floating(123) == 123
    assert floating(12.3) == 12.3

def test_integer():
    assert integer("123") == 123
    assert integer(123) == 123

def test_json():
    assert json('1') == 1
    assert json('"a"') == "a"
    assert json("[1, 2, 3]") == [1, 2, 3]

def test_number():
    assert number('123') == 123
    assert isinstance(number('123'), int)
    assert number('12.2') == 12.2
    assert isinstance(number('12.2'), float)

def test_string():
    assert string(123) == "123"
    assert string("123") == "123"
