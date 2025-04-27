from quix.core.opcodes import input, loop
from quix.memoptix import get_ref_scopes
from quix.memoptix.opcodes import free


def test_simple() -> None:
    program = [
        input(1),
        input(1),
        input(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 2)}


def test_simple_with_two_vars() -> None:
    program = [
        input(1),
        input(1),
        input(2),
        input(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 3), 2: (2, 3)}


def test_simple_with_free() -> None:
    program = [
        input(1),
        input(1),
        free(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 2)}


def test_three_vars_free() -> None:
    program = [
        input(1),
        input(1),
        input(2),
        free(1),
        input(3),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 3), 2: (2, 4), 3: (4, 4)}


def test_loop_two_var() -> None:
    program = [
        input(1),
        input(1),
        loop(
            1,
            [
                input(2),
            ],
        ),
        input(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 5), 2: (2, 5)}


def test_loop_enclosed_two_var() -> None:
    program = [
        input(1),
        input(1),
        loop(
            1,
            [
                input(2),
                free(2),
            ],
        ),
        input(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 6), 2: (3, 4)}


def test_double_loop() -> None:
    program = [
        input(1),
        input(1),
        loop(
            1,
            [
                input(2),
                loop(
                    1,
                    [
                        free(2),
                    ],
                ),
                input(1),
            ],
        ),
        input(1),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 9), 2: (3, 6)}


def test_complex() -> None:
    program = [
        input(1),
        input(1),
        loop(
            1,
            [
                input(2),
                loop(
                    3,
                    [
                        input(2),
                        free(2),
                    ],
                ),
                input(3),
            ],
        ),
        free(1),
        input(3),
    ]
    scopes = get_ref_scopes(program)
    assert scopes == {1: (0, 10), 2: (3, 7), 3: (2, 11)}
