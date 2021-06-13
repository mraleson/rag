import pytz
import pytest
from datetime import datetime as dt, timezone
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
from rag.validation.converters.datetime import datetime


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

def test_datetime():
    assert datetime(1623554331) == dt(2021, 6, 13, 3, 18, 51, tzinfo=timezone.utc)
    assert datetime("1623554331") == dt(2021, 6, 13, 3, 18, 51, tzinfo=timezone.utc)
    # datetime with tz
    assert datetime(dt(2021, 6, 13, 3, 18, 51, tzinfo=timezone.utc)) == \
           dt(2021, 6, 13, 3, 18, 51, tzinfo=timezone.utc)
    # datetime without tz (assumed utc)
    assert datetime(dt(2021, 6, 13, 3, 18, 51)) == \
           dt(2021, 6, 13, 3, 18, 51, tzinfo=timezone.utc)
    # js
    assert datetime("2021-06-13T03:23:42.244Z") == \
           dt(2021, 6, 13, 3, 23, 42, 244000, tzinfo=timezone.utc)
    # datetime.utcnow().isoformat()
    assert datetime("2021-06-13T03:24:34.088658") == \
           dt(2021, 6, 13, 3, 24, 34, 88658, tzinfo=timezone.utc)
    # datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    assert datetime("2021-06-13T03:27:24.995103+00:00") == \
           dt(2021, 6, 13, 3, 27, 24, 995103, tzinfo=timezone.utc)
    # datetime.now(pytz.timezone('US/Mountain')).isoformat()
    assert datetime("2021-06-12T21:30:09.287672-06:00") == \
           dt(2021, 6, 13, 3, 30, 9, 287672, tzinfo=timezone.utc)
