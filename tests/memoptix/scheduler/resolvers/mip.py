from quix.memoptix.scheduler import Array, Blueprint, HardLink, Index, LifeCycle, MIPResolver, Owner, SoftLink


def test_lifecycles_non_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraints(o1, LifeCycle(1, 10)).add_constraints(o2, LifeCycle(11, 15))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 0}


def test_lifecycles_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraints(o1, LifeCycle(1, 10)).add_constraints(o2, LifeCycle(7, 15))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 1, o2: 0}


def test_array() -> None:
    o1 = Owner("o1")

    bp = Blueprint().add_constraints(o1, Array(1))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 0}


def test_index() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraints(o1, Index(1)).add_constraints(o2, Index(10))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 1, o2: 10}


def test_lifecycles_with_array_non_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraints(o1, LifeCycle(1, 10))
        .add_constraints(o2, LifeCycle(11, 15))
        .add_constraints(o2, Array(100))
    )
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 0}


def test_lifecycles_with_array_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraints(o1, LifeCycle(1, 10))
        .add_constraints(o2, LifeCycle(7, 15))
        .add_constraints(o2, Array(100))
    )
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 0, o2: 1}


def test_lifecycles_with_array_index_overlapping() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = (
        Blueprint()
        .add_constraints(o1, LifeCycle(1, 10))
        .add_constraints(o2, LifeCycle(7, 15))
        .add_constraints(o2, Array(100))
        .add_constraints(o2, Index(0))
    )
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 100, o2: 0}


def test_hard_link() -> None:
    o1, o2 = Owner("o1"), Owner("o2")

    bp = Blueprint().add_constraints(o1, HardLink(o2, 10))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 10, o2: 0}


def test_soft_link() -> None:
    o1, o2, o3 = Owner("o1"), Owner("o2"), Owner("o3")

    bp = Blueprint().add_constraints(o1, SoftLink({o2: 5, o3: 7}))
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 7, o2: 2, o3: 0}


def test_soft_link_with_lifecycles() -> None:
    o1, o2, o3, o4 = Owner("o1"), Owner("o2"), Owner("o3"), Owner("o4")

    bp = (
        Blueprint()
        .add_constraints(o1, SoftLink({o2: 5, o3: 7}))
        .add_constraints(o1, SoftLink({o4: 5}))
        .add_constraints(o4, LifeCycle(1, 10))
        .add_constraints(o2, LifeCycle(7, 12))
    )
    ly = MIPResolver()(bp)
    assert ly.mapping() == {o1: 14, o2: 4, o3: 0, o4: 9}
