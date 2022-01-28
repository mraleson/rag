import pytest
import datetime
from django.utils import timezone
from unittest.mock import patch, Mock
from rag.validation import *

a = {}
b = {"a": 1}
c = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
d = {"b": {"d": {"e": 3}}}
e = {"a": 1, "b": {"c": 2, "d": 3}}

def test_validator():
    assert v.to.string.execute("1") == "1"
    assert v.to.integer.execute("1") == 1
    assert v.to.string.execute(1) == "1"
    assert v.to.integer.execute(1) == 1

    assert v.am.integer.execute(1) == 1
    assert v.am.string.execute("1") == "1"
    with pytest.raises(ValidationError): v.am.integer.execute("1")
    with pytest.raises(ValidationError): v.am.string.execute(1)
    assert v.to.string.am.string.to.integer.am.integer.execute(1) == 1

    assert len(v.am.chain) == 1
    assert len(v.to.chain) == 1
    assert len(v.accepts.chain) == 1
    assert len(v.optional.chain) == 1

def test_dig():
    with pytest.raises(KeyError): dig(None, 'a')
    with pytest.raises(KeyError): dig(1, 'a')
    with pytest.raises(KeyError): dig({'1': 1}, 'a')
    with pytest.raises(KeyError): dig({'1': {'3': 'b'}}, ['1', '2'])
    with pytest.raises(KeyError): dig({'1': {'2': 'b'}}, ['1', '2', '3'])
    assert dig({'1': None}, '1') is None
    assert dig({'1': 1}, '1') == 1
    assert dig({'1': 1}, ['1']) == 1
    assert dig({'1': 'a'}, '1') == 'a'
    assert dig({'1': {'2': 'b'}}, ['1', '2']) == 'b'

def test_accepts():
    errors, valid = check({}, {"a": v.accepts})
    assert errors == {"a": 'expected_defined'} and valid == {}

    errors, valid = check({'a': None}, {"a": v.accepts.null})
    assert errors == {} and valid == {'a': None}

    errors, valid = check({'a': None}, {"a": v.accepts.null.am.integer})
    assert errors == {} and valid == {'a': None}

    errors, valid = check({'a': 1}, {"a": v.accepts.null.am.integer})
    assert errors == {} and valid == {'a': 1}

    errors, valid = check({'a': None}, {"a": v.accepts.am.integer})
    assert errors == {"a": 'expected_integer'} and valid == {}

    errors, valid = check({'a': 'hi'}, {'a': v.accepts.any(['hi']).integer})
    assert errors == {} and valid == {'a': 'hi'}

    errors, valid = check({'a': 'bye'}, {'a': v.accepts.any(['hi']).integer})
    assert errors == {"a": 'expected_integer'} and valid == {}

    errors, valid = check({'a': 'bye'}, {'a': v.accepts.any(['hi', 'bye']).integer})
    assert errors == {} and valid == {'a': 'bye'}

def test_skips():
    errors, valid = check({"a": 1}, {"a": v.skips.blank.am.integer})
    assert errors == {} and valid == {"a": 1}

    errors, valid = check({"a": ''}, {"a": v.skips.blank.am.integer})
    assert errors == {} and valid == {}

    errors, valid = check({"a": "b"}, {"a": v.skips.blank.am.integer})
    assert errors == {"a": 'expected_integer'} and valid == {}

    errors, valid = check({"a": 2}, {"a": v.skips.any([2]).am.integer})
    assert errors == {} and valid == {}

    errors, valid = check({"a": []}, {"a": v.skips.empty.am.integer})
    assert errors == {} and valid == {}

    errors, valid = check({"a": 6}, {"a": v.skips.equals(5, 6).am.integer})
    assert errors == {} and valid == {}

    errors, valid = check({"a": None}, {"a": v.skips.null.am.integer})
    assert errors == {} and valid == {}


def test_validate():
    errors, valid = check({}, {"a": v.am})
    assert errors == {"a": 'expected_defined'} and valid == {}

    errors, valid = check({"a": "b"}, {"a": v.am})
    assert errors == {} and valid == {"a": "b"}

    errors, valid = check({"a": "b"}, {"a": v.am.integer})
    assert errors == {"a": 'expected_integer'} and valid == {}

    errors, valid = check({"a": 1}, {"a": v.am.integer})
    assert errors == {} and valid == {"a": 1}

def test_convert():
    errors, valid = check({}, {"a": v.to})
    assert errors == {"a": 'expected_defined'} and valid == {}

    errors, valid = check({"a": 1}, {"a": v.to})
    assert errors == {} and valid == {"a": 1}

    errors, valid = check({"a": 1}, {"a": v.to.string.am.string})
    assert errors == {} and valid == {"a": "1"}

    errors, valid = check({"a": 1}, {"a": v.to.string.am.string.to.integer.am.integer})
    assert errors == {} and valid == {"a": 1}

def test_optional():
    errors, valid = check({}, {"a": v.optional})
    assert errors == {} and valid == {}

    errors, valid = check({"a": "b"}, {"a": v.optional.string})
    assert errors == {} and valid == {"a": "b"}

    errors, valid = check({"a": 1}, {"a": v.optional.string})
    assert errors == {"a": "expected_string"} and valid == {}

def test_check():
    errors, valid = check({}, {})
    assert errors == {} and valid == {}

    errors, valid = check(c, {"a": v.am, "b": {"c": v.am, "d": {"e": v.am}}})
    assert errors == {} and valid == c

    errors, valid = check(c, {"a": v.am, "b": {"c": v.am, "d": {"e": v.am, "f": v.am}}})
    assert errors == {"b": {"d": {"f": "expected_defined"}}} and valid == c

@pytest.mark.skip
def test_validate_data():
    response = self.post("/vecho", c)
    assert response.status_code == 200
    assert response.data == c

    response = self.post("/vecho", b)
    assert response.status_code == 400
    assert response.data == {'b': {'c': 'expected_defined', 'd': 'expected_defined'}}

@pytest.mark.skip
def test_validate_query():
    response = self.get("/vquery", {'age': 12})
    assert response.status_code == 200
    assert response.data == {'age': 12}
    #
    # response = self.get("/vparams/12", b)
    # assert response.status_code == 400
    # assert response.data == {'b': {'c': 'expected_defined', 'd': 'expected_defined'}}

# we could have validate package up args and kwargs, then unpackage them and pass to view
# after validation, I think its the right way to go just maybe not that useful of a feature
# and it is a bit strange to have a url 400 based on the url so theres that too
# def test_validate_url_params():
#     response = self.get("/vpurl", c)
#     assert response.status_code == 404
#
#     response = self.get("/vpurl/12", c)
#     assert response.status_code == 200
#     assert response.data == {'num': '12'}
