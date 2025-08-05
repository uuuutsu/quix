import pytest

from quix.memoptix.scheduler import Array, Index, Layout, Node, SimpleSlider


def test_incompatible_layouts() -> None:
    node1 = Node((0, 10), ref="o1").add_constraint(Index(0))
    node2 = Node((0, 10), ref="o2").add_constraint(Index(0))
    l1 = Layout({node1: 0}, nodes=[node1])
    l2 = Layout({node2: 0}, nodes=[node2])

    with pytest.raises(RuntimeError):
        SimpleSlider()(l1, l2)


def test_compatible_layouts() -> None:
    node1 = Node((0, 10), ref="o1").add_constraint(Index(0))
    node2 = Node((0, 10), ref="o2")
    l1 = Layout({node1: 0}, nodes=[node1])
    l2 = Layout({node2: 0}, nodes=[node2])

    assert SimpleSlider()(l1, l2).mapping() == {node1: 0, node2: 1}


def test_compatible_array_layouts() -> None:
    node1 = Node((0, 10), ref="o1").add_constraint(Index(0)).add_constraint(Array(100))
    node2 = Node((0, 10), ref="o2")
    l1 = Layout({node1: 0}, nodes=[node1])
    l2 = Layout({node2: 0}, nodes=[node2])

    assert SimpleSlider()(l1, l2).mapping() == {node1: 1, node2: 0}
