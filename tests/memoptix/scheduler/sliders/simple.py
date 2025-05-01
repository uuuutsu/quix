import pytest

from quix.memoptix.scheduler import Array, Blueprint, Index, Layout, LifeCycle, Owner, SimpleSlider


def test_incompatible_layouts() -> None:
    o1, o2 = Owner("o1"), Owner("o2")
    l1 = Layout(Blueprint().add_constraints(o1, Index(0)).add_constraints(o1, LifeCycle(0, 10)), {o1: 0})
    l2 = Layout(Blueprint().add_constraints(o2, Index(0)).add_constraints(o2, LifeCycle(0, 10)), {o2: 0})

    with pytest.raises(RuntimeError):
        SimpleSlider()(l1, l2)


def test_compatible_layouts() -> None:
    o1, o2 = Owner("o1"), Owner("o2")
    l1 = Layout(Blueprint().add_constraints(o1, Index(0)).add_constraints(o1, LifeCycle(0, 10)), {o1: 0})
    l2 = Layout(Blueprint().add_constraints(o2, LifeCycle(0, 10)), {o2: 0})

    assert SimpleSlider()(l1, l2).mapping() == {o1: 0, o2: 1}


def test_compatible_array_layouts() -> None:
    o1, o2 = Owner("o1"), Owner("o2")
    l1 = Layout(
        Blueprint().add_constraints(o1, Index(0)).add_constraints(o1, LifeCycle(0, 10)).add_constraints(o1, Array(100)),
        {o1: 0},
    )
    l2 = Layout(Blueprint().add_constraints(o2, LifeCycle(0, 10)), {o2: 0})

    assert SimpleSlider()(l1, l2).mapping() == {o1: 1, o2: 0}
