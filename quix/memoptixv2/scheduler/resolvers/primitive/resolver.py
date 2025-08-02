from typing import override

from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.resolvers.base import Resolver
from quix.memoptixv2.scheduler.tree import Array, Index, Node
from quix.memoptixv2.scheduler.tree.flatten import flatten_node
from quix.tools import intervals_intersects

from .utils import extract_constraint_info, get_all_affected_nodes, order_ascend_with_array_in_the_back


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __domain__ = {Index, Array}

    @override
    def __call__(self, node: Node) -> Layout:
        indexes, arrays = extract_constraint_info(node)
        ordered_nodes = order_ascend_with_array_in_the_back(arrays)

        mapping: dict[Node, int] = {}
        for node, index in indexes.items():
            mapping[node] = index

        for node in ordered_nodes:
            if node in mapping:
                continue

            index = 0
            while True:
                curr_nodes = get_all_affected_nodes(node, mapping, index, arrays)
                for curr_node in curr_nodes:
                    if not intervals_intersects(curr_node.lifecycle, node.lifecycle):
                        continue
                    break
                else:
                    mapping[node] = index
                    break
                index += 1

        for node_ in set(flatten_node(node).keys()).difference(mapping):
            mapping[node_] = 0

        return Layout(mapping, [node])
