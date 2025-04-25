from quix.scheduler import Array, Blueprint, Index, LifeCycle, Owner, PrimitiveResolver


def test_lifecycles_non_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraint(o1, LifeCycle(1, 10)).add_constraint(o2, LifeCycle(11, 15))
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 0}


def test_lifecycles_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraint(o1, LifeCycle(1, 10)).add_constraint(o2, LifeCycle(7, 15))
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 1}


def test_array() -> None:
    o1 = Owner("o1")

    bp = Blueprint().add_constraint(o1, Array(1))
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 0}


def test_index() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraint(o1, Index(1)).add_constraint(o2, Index(10))
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 1, o2: 10}


def test_lifecycles_with_array_non_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraint(o1, LifeCycle(1, 10))
        .add_constraint(o2, LifeCycle(11, 15))
        .add_constraint(o2, Array(100))
    )
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 0}


def test_lifecycles_with_array_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraint(o1, LifeCycle(1, 10))
        .add_constraint(o2, LifeCycle(7, 15))
        .add_constraint(o2, Array(100))
    )
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 1}


def test_lifecycles_with_array_index_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraint(o1, LifeCycle(1, 10))
        .add_constraint(o2, LifeCycle(7, 15))
        .add_constraint(o2, Array(100))
        .add_constraint(o2, Index(0))
    )
    ly = PrimitiveResolver()(bp)
    assert ly.mapping() == {o1: 101, o2: 0}
