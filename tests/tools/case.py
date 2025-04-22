import pytest

from quix.tools.case import pascal_case_to_snake_case, snake_case_to_pascal_case


@pytest.mark.parametrize(
    "actual,target",
    [
        ("first_name", "FirstName"),
        ("data_value", "DataValue"),
        ("my__name_Is_", "MyNameIs"),
        ("____Class", "Class"),
    ],
)
def test_snake2camel(actual: str, target: str) -> None:
    assert snake_case_to_pascal_case(actual) == target


@pytest.mark.parametrize(
    "actual,target",
    [
        ("DummyValue", "dummy_value"),
        ("__Data", "data"),
        ("ThatIs__Crazy", "that_is___crazy"),
        ("snake_case", "snake_case"),
    ],
)
def test_camel2snake(actual: str, target: str) -> None:
    assert pascal_case_to_snake_case(actual) == target
