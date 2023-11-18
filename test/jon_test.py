import pytest
from src.peekable import peekable
from src.jon import parse_token, loads

# test case parameters
test_data = [
    ("'token'", "'token'"),
    ('"token"', '"token"'),
    ('"tok\\\'en"', '"tok\\\'en"'),
    ('token ', 'token'),
    (' ', ''),
    ('tok{}:,en', 'tok'),
    ('  token', ''),
    ('tok\\ en', 'tok en'),
    ('tok\\:en', 'tok:en'),
    ('tok\\ten', 'tok\ten'),
    ('tok\\nen', 'tok\nen'),
]

@pytest.mark.parametrize("code_str,expected_output", test_data)
def test_parse_token(code_str, expected_output):
    assert parse_token(peekable(code_str)) == expected_output

json_test_data = [("{}", {}),
  ('{"key": "value"}', {"key": "value"}),
  ('{"key1": "value1", "key2": "value2"}', {"key1": "value1", "key2": "value2"}),
  ('{"parent": {"child": "value"}}', {"parent": {"child": "value"}}),
  ('{"parent": {"child": "value"}}', {"parent": {"child": "value"}}),
  ('{"parent": {"child1": "value1", "child2": "value2"}}', {"parent": {"child1": "value1", "child2": "value2"}}),
  ('{"array": [1, 2, 3]}', {"array": [1, 2, 3]}),
  ('{"nullKey": null}', {"nullKey": None}),
  ('{"booleanKey": true}', {"booleanKey": True}),
  ('{"booleanKey": false}', {"booleanKey": False}),
  ('{"intKey": 1, "floatKey": 1.1}', {"intKey": 1, "floatKey": 1.1}),
  ('{"stringKey": "stringValue", "numberKey": 123}', {"stringKey": "stringValue", "numberKey": 123}),
  ('{"complexKey": {"subKey1": "subValue1", "subKey2": [1, 2, 3]}}', {"complexKey": {"subKey1": "subValue1", "subKey2": [1, 2, 3]}}),]

@pytest.mark.parametrize("code_str,expected_output", json_test_data)
def test_loads(code_str, expected_output):
    assert loads(code_str) == expected_output
