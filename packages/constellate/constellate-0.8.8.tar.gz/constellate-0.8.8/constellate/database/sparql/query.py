from typing import Dict
from rdflib import Graph
from rdflib.query import Result
from rdflib.store import Store


def query(
    raw_query: str,
    graph: Graph = None,
    store: Store = None,
    init_namespaces: Dict = None,
    init_bindings: Dict = None,
) -> Result:
    """
    Query a store, with provided query builder and bindings applied

    Usage: See unit tests
    """
    init_namespaces = init_namespaces or {}
    init_bindings = init_bindings or {}

    graph = Graph(store=store) if graph is None and store is None else graph
    return graph.query(raw_query, initNs=init_namespaces, initBindings=init_bindings)
