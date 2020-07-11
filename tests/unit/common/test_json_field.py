from unittest.mock import Mock

import pytest
from common.json_field import SQLiteJSONField


@pytest.mark.parametrize(
    "value, expected",
    (
        (
            '{"json": ["this", "is", "json", true], "test": null}',
            {"json": ["this", "is", "json", True], "test": None},
        ),
        (None, None),
    ),
)
def test_from_db_value(value, expected):
    field = SQLiteJSONField()

    result = field.from_db_value(value, None, None)

    assert result == expected


@pytest.mark.parametrize("value", (None, 17, True, {}, 'not"a@json'))
def test_to_python_wrong(value):
    field = SQLiteJSONField()

    result = field.to_python(value)

    assert result == value


def test_get_prep_value_wrong():
    field = SQLiteJSONField()

    result = field.get_prep_value(None)

    assert result is None


def test_value_to_string():
    field = SQLiteJSONField()
    field.attname = "settings"

    model = Mock()
    model.settings = "json_value"
    result = field.value_to_string(model)

    assert result == "json_value"
