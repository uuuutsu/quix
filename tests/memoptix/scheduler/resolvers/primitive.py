from quix.memoptix.scheduler import Array, Index, Node, PrimitiveResolver


def test_lifecycles_non_overlapping() -> None:
    node1 = Node((1, 10), ref="o1")

    ly = PrimitiveResolver()(node1)
    assert ly.mapping() == {node1: 0}


def test_lifecycles_overlapping() -> None:
    node1 = Node((1, 10), ref="o1")

    ly = PrimitiveResolver()(node1)
    assert ly.mapping() == {node1: 0}


def test_array() -> None:
    node1 = Node((1, 10), ref="o1").add_constraint(Array(1))

    ly = PrimitiveResolver()(node1)
    assert ly.mapping() == {node1: 0}


def test_index() -> None:
    node1 = Node((1, 10), ref="o1").add_constraint(Index(1))

    ly = PrimitiveResolver()(node1)
    assert ly.mapping() == {node1: 1}
