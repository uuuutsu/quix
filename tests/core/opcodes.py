from typing import Any

import pytest

from quix.core.opcodes import add, end_loop, inject, input, output, start_loop


@pytest.mark.parametrize(
    "args",
    [
        {"ref": 5, "value": 10},
        {"ref": 0, "value": -15},
    ],
)
def test_add(args: dict[str, Any]) -> None:
    assert add(**args).args() == args
    assert add(**args).__id__ == "add"
    assert add(**args).__class__.__name__ == "Add"


@pytest.mark.parametrize(
    "args",
    [
        {"ref": 5},
        {"ref": -10},
    ],
)
def test_input(args: dict[str, Any]) -> None:
    assert input(**args).args() == args
    assert input(**args).__id__ == "input"
    assert input(**args).__class__.__name__ == "Input"


@pytest.mark.parametrize(
    "args",
    [
        {"ref": 5},
        {"ref": -10},
    ],
)
def test_output(args: dict[str, Any]) -> None:
    assert output(**args).args() == args
    assert output(**args).__id__ == "output"
    assert output(**args).__class__.__name__ == "Output"


@pytest.mark.parametrize(
    "args",
    [
        {"ref": 5},
        {"ref": -10},
        {"ref": -10},
    ],
)
def test_start_loop(args: dict[str, Any]) -> None:
    assert start_loop(**args).args() == args
    assert start_loop(**args).__id__ == "start_loop"
    assert start_loop(**args).__class__.__name__ == "StartLoop"


def test_end_loop() -> None:
    assert end_loop().args() == {}
    assert end_loop().__id__ == "end_loop"
    assert end_loop().__class__.__name__ == "EndLoop"


@pytest.mark.parametrize(
    "args",
    [
        {"ref": 5, "code": "", "exit": 30, "sortable": True},
        {"ref": 0, "code": "sigma", "exit": -55, "sortable": False},
        {"ref": -1, "code": "that's crazy", "exit": 100, "sortable": True},
    ],
)
def test_inject(args: dict[str, Any]) -> None:
    assert inject(**args).args() == args
    assert inject(**args).__id__ == "inject"
    assert inject(**args).__class__.__name__ == "Inject"
