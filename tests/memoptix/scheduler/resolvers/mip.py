from quix.memoptix.scheduler import HardLink, Index, MIPResolver, Node, SoftLink


def test_lifecycles_non_overlapping() -> None:
    node1 = Node((11, 15), ref="o2")

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 0}


def test_array() -> None:
    node1 = Node((1, 10), ref="o1")

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 0}


def test_index() -> None:
    node1 = Node((1, 10), ref="o1").add_constraint(Index(1))

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 1}


def test_hard_link() -> None:
    node2 = Node((1, 10), ref="o2")
    node1 = Node((1, 10), ref="o1").add_constraint(HardLink(node2, 10))

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 10, node2: 0}


def test_soft_link() -> None:
    node2 = Node((1, 10), ref="o2")
    node3 = Node((1, 10), ref="o3")
    node1 = Node((1, 10), ref="o1").add_constraint(SoftLink({node2: 5, node3: 7}))

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 7, node2: 2, node3: 0}


def test_soft_link_with_lifecycles() -> None:
    node4 = Node((1, 10), ref="o4")
    node3 = Node((1, 10), ref="o3")
    node2 = Node((7, 12), ref="o2")
    node1 = Node((1, 10), ref="o1").add_constraint(SoftLink({node2: 5, node3: 7})).add_constraint(SoftLink({node4: 5}))

    ly = MIPResolver()(node1)
    assert ly.mapping() == {node1: 10, node2: 5, node3: 3, node4: 0}
