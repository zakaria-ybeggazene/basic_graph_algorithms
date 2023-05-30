from typing import Any
from flow import Flow
from network import NetworkType

Node = Any


def maximal_flow(network: NetworkType, s: Node, t: Node) -> Flow:
    """
    Renvoie le flot maximal sur le réseau `network` entre la source `s` et la cible `t`.

    INPUT :

        - network, un réseau de type Network
        - s, le sommet source
        - t, le sommet cible

    OUTPUT : un objet Flow de valeur maximale sur le réseau.
    """
    flow = Flow(network, s, t)
    path = flow.find_augmenting_path()
    while path:
        flow.increase_augmenting_path(path)
        path = flow.find_augmenting_path()
    return flow
