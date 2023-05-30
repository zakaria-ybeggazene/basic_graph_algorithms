# -*- coding: utf-8 -*-
"""A home-made class for graphs

This class implements a (tiny) subset of `networkx` features, trying
to retain compatibility, up to some exceptions. For example, the nodes
and edges methods of networkx return views rather than
sequences. also, the `edges` method is richer in `networkx`, but does
not include the capacity, nor reverse edges for undirected graphs.

We test the compatibility of the basic methods on all the examples::

    >>> import graph, graph_networkx
    >>>
    >>> for G, GN in zip( graph.examples.all(), graph_networkx.examples.all() ):
    ...    assert G.is_directed() == GN.is_directed()
    ...    assert tuple(G.nodes()) == tuple(GN.nodes())
    ...    assert G.number_of_nodes() == GN.number_of_nodes()
    ...    #assert G.number_of_edges() == GN.number_of_edges()
    ...    for v in G.nodes():
    ...        assert set(G.successors(v)) == set(GN.neighbors(v))
    ...    for v1, v2, c in G.edges():
    ...        assert GN.has_edge(v1, v2)
    ...    for v1, v2 in GN.edges():
    ...        assert G.has_edge(v1, v2)
    ...    H = G.networkx()
    ...    assert H.nodes() == GN.nodes()
    ...    assert H.edges() == GN.edges()
    ...    assert H.is_directed() == GN.is_directed()

"""

from typing import Any, Dict, List, Optional, Sequence
import networkx  # type: ignore
import graph_examples
from graph_networkx import Node, Capacity, Edge


class Graph:

    # Déclaration des attributs
    # La structure de donnée et l'initialisation vous est donnée
    # pour les sommets (nodes) et pour le choix orienté ou non (directed)
    _nodes: List[Node]
    _node_indices: Dict[Node, int]
    _directed: bool
    # À vous de choisir la structure de donnée pour les arêtes (edges)
    # Remplacer la ligne suivante par le code adéquat
    _edges: Dict[Node, Dict[Node, Capacity]]

    def __init__(
        self,
        nodes: Optional[Sequence[Node]] = None,
        matrix: Optional[List[List[int]]] = None,
        edges: Optional[Sequence[Edge]] = None,
        directed: bool = False,
    ):
        """
        Initialisation d'un graphe

        INPUT :

            - nodes, un itérable sur les sommets du graphes
            - matrix, la matrice d'adjacence du graphe suivant les
              mêmes indices que `nodes`
            - edges, une liste de triplets (v1, v2, c) où v1 et v2
              sont des sommets et c un nombre positif

        """
        if nodes is None:
            nodes = []

        self._nodes = list(nodes)
        # création d'un dictionnaire associant son indice à chaque sommet
        # (vous pouvez modifier si ça n'est pas utile à votre implantation)
        self._node_indices = {nodes[i]: i for i in range(len(nodes))}
        self._directed = directed

        # on ne peut pas donner à la fois matrix et edges
        if matrix is not None and edges is not None:
            raise ValueError(
                "'matrix' et 'edges' ne peuvent pas être tous les deux initialisés"
            )

        # Les méthodes _init_xxx sont responsables de
        # l'initialisation de la structure de donnée
        # pour les arêtes en fonction du type d'entrée
        if matrix is not None:
            self._init_from_matrix(matrix)
        elif edges is not None:
            self._init_from_edges(edges)
        else:
            self._init_empty()

    def _init_empty(self) -> None:
        """
        Initialisation pour un graphe vide (sans arêtes)
        """
        self._edges = dict()

    def _init_from_matrix(self, matrix: Sequence[Sequence[Capacity]]) -> None:
        """
        Initialisation à partir d'une matrice

        EXAMPLES:

            >>> M = matrix = [[0, 12,  0, 12],
            ...               [0,  0, 23, 0],
            ...               [0,  0,  0, 0],
            ...               [0,  0,  0, 0]]
            >>> G = Graph(nodes = ["A", "B", "C", "D"],
            ...           matrix = M,
            ...           directed = True)
            >>> G.edges()
            (('A', 'B', 12), ('A', 'D', 12), ('B', 'C', 23))
            >>> G.matrix() == M
            True
        """
        assert isinstance(matrix, Sequence), "matrix has to be of type Sequence"
        if not matrix:
            self._edges = dict()
        assert all([isinstance(i, Sequence) for i in matrix]), \
            "all elements of matrix have to be of type Sequence"
        length = len(matrix[0])
        assert all([len(i) == length for i in matrix]), \
            "all Sequence elements of matrix have to be of same length"
        self._edges = {self._nodes[i]:
                       {self._nodes[j]: matrix[i][j]
                        for j in range(length) if matrix[i][j] != 0}
                       for i in range(length)}

    def _init_from_edges(self, edges: Sequence[Edge]) -> None:
        """
        Initialisation à partir d'une liste de triplets
        """
        assert isinstance(edges, Sequence), "edges has to be of type Squence"
        if not edges:
            self._edges = dict()
        assert all([isinstance(i, tuple) for i in edges]), \
            "all elements of edges have to be of type Tuple"
        assert all([c != 0 for (_, _, c) in edges]), \
            "all capacities have to be different from 0"
        res: Dict[Node, Dict[Node, Capacity]] = {}
        for (i, j, c) in edges:
            if not res.get(i):
                res.update({i: {}})
            res[i].update({j: c})
            if not self._directed:
                if not res.get(j):
                    res.update({j: {}})
                res[j].update({i: c})
        self._edges = res

    def is_directed(self) -> bool:
        """
        Renvoie si le graph est orienté
        """
        return self._directed

    def set_edge_capacity(self, v1: Node, v2: Node, c: Capacity) -> None:
        """
        Donne la capacité `c` à l'arête `(v1,v2)`

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe
            - c la capacité de l'arête (v1,v2)

        EXAMPLES:

            >>> G = GG = Graph(edges = [(1,2,1)], nodes = [1,2], directed = True)
            >>> G.set_edge_capacity(1,2,2)
            >>> G.edges()
            ((1, 2, 2),)
        """
        l1 = self._edges.get(v1)
        if l1:
            l2 = l1.get(v2)
            if l2:
                l1.update({v2: c})
        else:
            raise ValueError(f"Edge ({v1},{v2}) must exist")

    def add_node(self, v: Node) -> None:
        """
        Ajoute le sommet `v` au graphe

        INPUT:

            - v, un sommet du graphe

        Complexity:
        Constant
        """
        if v not in self._node_indices:
            i = len(self._nodes)
            self._node_indices.update({v: i})
            self._nodes.append(v)
        else:
            raise ValueError(f"Node {v} already exists")

    def nodes(self) -> Sequence[Node]:
        """
        Renvoie la liste des sommets du graphe

        EXAMPLES:

            >>> from graph import examples
            >>> G = examples.cours_1_reseau()
            >>> G.nodes()
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        Complexity:
        Constant
        """
        return self._nodes
    
    vertices = nodes

    def number_of_nodes(self) -> int:
        """
        Renvoie le nombre de sommets du graphe

        EXAMPLES:

            >>> G = examples.cours_1_reseau()
            >>> G.number_of_nodes()
            8

        Complexity:
        Constant
        """
        return len(self._nodes)

    def has_node(self, v1: Node) -> bool:
        """
        Renvoie vrai si v1 est un sommet du graphe

        INPUT:

            - v1, un sommet

        Complexity:
        Constant
        """
        return v1 in self._node_indices

    def edges(self) -> Sequence[Edge]:
        """
        Renvoie les arêtes de ce graphe avec leurs capacités

        Chaque arête est renvoyée comme un triplet `(v1, v2, c)`.

        EXAMPLES:

            >>> G = Graph((1,2,3,4))
            >>> G. edges()
            ()
            >>> G = examples.directed()
            >>> G.edges()
            ((1, 2, 12), (1, 4, 12), (2, 3, 23))

            >>> G = examples.undirected()
            >>> G.edges()
            ((1, 2, 12), (2, 1, 12), (2, 3, 23), (3, 2, 23))

        Complexity:
        Given that n is the number of nodes in the graph, complexity is o(n^2) ?
        """
        return tuple([(i, j, c) for i, d in self._edges.items()
                      for j, c in d.items()])

    def number_of_edges(self) -> int:
        """
        Renvoie le nombre d'arêtes du graphe

        Complexity:
        Given that n is the number of nodes, number_of_edges has complexity of o(n)
        Alternatively we could store this information as an attribute.
        """
        return sum([len(d) for _, d in self._edges.items()])

    def has_edge(self, v1: Node, v2: Node) -> bool:
        """
        Renvoie True si l'arête (v1,v2) existe

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe

        Complexity:
        Constant
        """
        return v2 in self.successors(v1)

    def capacity(self, v1: Node, v2: Node) -> Capacity:
        """
        Renvoie la capacité de l'arête (v1,v2)

        Si l'arête n'existe pas, la capacité est 0.

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe

        EXAMPLES:

            >>> G = examples.directed()
            >>> G.capacity(1,2)
            12
            >>> G.capacity(2,1)
            0
            >>> G.capacity(2,3)
            23
            >>> G.capacity(3,2)
            0

        Complexity:
        Constant
        """
        d = self._edges.get(v1)
        if d is None:
            return 0
        c = d.get(v2)
        if c is None:
            return 0
        return c

    def matrix(self) -> List[List[Capacity]]:
        """
        Retourne la matrice associée au graphe

        Soit `n` le nombre de sommets du graphe. Cette méthode renvoie
        une liste `M` de n listes de taille n, de sorte que `M[i][j]`
        est la capacité de l'arête reliant le i-ème sommet au j-ème
        sommet dans le graphe, s'il y en a une, et 0 sinon.

        EXAMPLES:

            >>> G = examples.directed()
            >>> G.matrix()
            [[0, 12, 0, 12], [0, 0, 23, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        Complexity:
        We call a o(1) operation n*n times, implies complexity is o(n^2)
        """
        return [[self.capacity(v1, v2) for v2 in self.nodes()] for v1 in self.nodes()]

    def to_dict(self) -> Dict:
        """
        Retourne le dictionnaire associé au graphe
        """
        return self._edges

    def predecessors(self, v: Node) -> Sequence[Node]:
        """
        Renvoie la liste des voisins entrants de `v`

        INPUT:

            - v, un sommet du graphe

        EXAMPLES:

            >>> G = examples.cours_1_reseau()
            >>> sorted(G.predecessors("H"))
            ['C', 'D', 'E', 'G']
            >>> G = examples.directed()
            >>> G.predecessors(1)
            []
            >>> G.predecessors(2)
            [1]

        Complexity:
        Given that n is the number of nodes in the graph, the complexity is o(n)
        or constant in case the graph is underected (predecessors corresponds
        to successors).
        """
        if self._directed:
            return [i for i, d in self._edges.items() if v in d]
        else:
            return self.successors(v)

    def successors(self, v: Node) -> Sequence[Node]:
        """
        Renvoie la liste des voisins sortants de `v`

        INPUT:

            - v, un sommet du graphe

        EXAMPLES:

            >>> G = examples.cours_1_reseau()
            >>> sorted(G.successors("A"))
            ['B', 'F', 'G']
            >>> G = examples.directed()
            >>> sorted(G.successors(1))
            [2, 4]
            >>> G.successors(2)
            [3]
            >>> G.successors(4)
            []

        Complexity:
        Constant
        """
        if self._edges.get(v):
            return list(self._edges[v].keys())
        else:
            return []

    neighbors = successors

    def is_path(self, p: Sequence[Node]) -> bool:
        """
        Renvoie True si `p` est un chemin valide dans le graphe

        INPUT:

            - p, une liste de sommets du graphe

        EXAMPLES:

            >>> G = examples.cours_1_reseau()
            >>> G.is_path([])
            True
            >>> G.is_path(["D"])
            True
            >>> G.is_path(["D", "G"])
            False
            >>> G.is_path(["D", "H"])
            True
            >>> G.is_path(["D", "H", "F"])
            False
            >>> G.is_path(["D", "H", "G", "B", "A"])
            True

        Complexity:
        Given that n is the number of nodes in p, the complexity is of o(n)
        """
        assert isinstance(p, Sequence), "p has to be of type Sequence"
        if not p:
            return True
        elif len(p) == 1:
            return True
        else:
            return p[1] in self.successors(p[0]) and self.is_path(p[1:])

    def networkx(self) -> networkx.Graph:
        """
        Return a networkx graph with the same nodes and edges
        """
        import graph_networkx

        return graph_networkx.Graph(
            self.nodes(), self.edges(), directed=self.is_directed()
        )

    def show(self) -> Any:
        """
        Display the current graph
        """
        return self.networkx().show()
    
    def parcours_en_profondeur(self, u: Node) -> Dict[Node, int]:
        """
        INPUT:
        - 'self' - un graphe
        - 'u' - un sommet du graphe

        OUTPUT: un dictionnaire associant à chaque sommet `v` accessible depuis `u` sa distance depuis `u`
        """
        distances = {u: 0} # L'ensemble des sommets déjà rencontrés
        todo      = [u]    # Une liste de sommets à traiter

        while todo:
            # Invariants:
            # - Si `v` est dans `distances`, alors il y a un chemin de `u` à `v`,
            #   et distances[v] contient la distance de `u` à `v`;
            # - Si `v` est dans `distances` et pas dans `todo`
            #   alors tous les voisins de `v` sont dans `distances`
            v = todo.pop()
            for w in self.neighbors(v):
                if w not in distances:
                    distances.update({w: 1+distances[v]})
                    todo.append(w)
        return distances

    ######################################################################
    # Partie sur les cycles dans un graphe à copier dans votre solution
    ######################################################################
    def is_cycle(self, c):
        """
        Renvoie si `c` est un chemin valide dans le graphe

        INPUT:

            - c, une liste de sommets du graphe

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> G.is_cycle([])
            False
            >>> G.is_cycle(["D"])
            False
            >>> G.is_cycle(["D", "G"])
            False
            >>> G.is_cycle(["D", "H"])
            False
            >>> G.is_cycle(["D", "H", "C"])
            True
            >>> G.is_cycle(["A", "G", "F"])
            True
            >>> G.is_cycle(["D", "H", "G", "B", "A", "F", "E"])
            True
            >>> G.is_cycle(["C", "G", "B", "A", "G", "H"])
            False
        """
        if not len(c) > 2:
            return False
        unique = set()
        if any(i in unique or unique.add(i) for i in c):
            return False
        it = iter(c)
        u = next(it, None)
        
        for v in it:
            if not self.has_edge(u, v):
                return False
            u = v
        return self.has_edge(c[0], u)
            

    def connected_components(self):
        """
        Renvois les composantes connexe du graphe

        OUTPUT:

            - une liste d'ensemble de noeuds

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> CCG = G.connected_components()
            >>> len(CCG)
            1
            >>> sorted(list(CCG[0]))
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            >>> examples.undirected().connected_components()
            [{1, 2, 3}, {4}]
            >>> examples.disconnected().connected_components()
            [{1, 2, 5}, {3, 4}]
        """
        seen = set()
        result = []
        for node in self.nodes():
            if node not in seen:
                cc = set()
                todo = set([node])
                while todo:
                    u = todo.pop()
                    seen.add(u)
                    todo.update(set(self.neighbors(u)) - seen)
                    cc.add(u)
                result.append(cc)
        return result
                

    def is_connected(self):
        """
        Renvoie si le graphe est connexe

        EXAMPLES::

            >>> examples.cours_1_reseau().is_connected()
            True
            >>> examples.undirected().is_connected()
            False
            >>> examples.disconnected().is_connected()
            False
            >>> examples.tree1().is_connected()
            True
        """
        #num_edges = self.number_of_edges()
        #if not self._directed:
        #    num_edges /= 2
        #if num_edges < self.number_of_nodes() - 1:
        #    return False
        if len(self.parcours_en_profondeur(self._nodes[0])) == self.number_of_nodes():
            return True
        else:
            return False

    def is_acyclic(self):
        """
        Renvoie si le graphe est acyclique

        EXAMPLES::

            >>> examples.cours_1_reseau().is_acyclic()
            False
            >>> examples.undirected().is_acyclic()
            True
            >>> examples.disconnected().is_acyclic()
            True
            >>> examples.lines().is_acyclic()
            True
        """
        k = len(self.connected_components())
        if self._directed:
            return self.number_of_nodes() == k + self.number_of_edges()
        else:
            return self.number_of_nodes() == k + (self.number_of_edges() / 2)

    def is_tree(self):
        """
        Renvoie si le graphe est un arbre

        EXAMPLES::

            >>> examples.cours_1_reseau().is_tree()
            False
            >>> examples.undirected().is_tree()
            False
            >>> examples.disconnected().is_tree()
            False
            >>> examples.tree1().is_tree()
            True
            >>> examples.lines().is_tree()
            False
        """
        if self._directed:
            return self.is_connected() and self.number_of_edges() == (self.number_of_nodes() - 1)
        else:
            return self.is_connected() and (self.number_of_edges() / 2) == (self.number_of_nodes() - 1)
    def find_cycle(self):
        """
        Renvoie un cycle du graphe

        OUTPUT:

            - une liste ou None si le graphe est acyclique

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> G.is_cycle(G.find_cycle())
            True

            >>> G = examples.G2()
            >>> G.is_cycle(G.find_cycle())
            True

            >>> examples.undirected().find_cycle() is None
            True
            >>> examples.disconnected().find_cycle() is None
            True

            >>> for t in examples.trees():
            ...     assert(t.find_cycle() is None)

            >>> for G in examples.cyclic():
            ...     assert(G.is_cycle(G.find_cycle()))
        """
        cycle = None
        for u in self._nodes:
            seen = set([u])       # L'ensemble des sommets déjà rencontrés
            chemin = {u: u}
            todo      = [u]    # Une liste de sommets à traiter
            while todo:
                v = todo.pop()
                for w in self.neighbors(v):
                    if w not in seen:
                        chemin.update({w: v})
                        todo.append(w)
                        seen.add(w)
                    elif chemin[v] != w:
                        cycle = [chemin[w], w]
                        p = v
                        while p != chemin[w]:
                            if p:
                                cycle.append(p)
                                p = chemin[p]
                            else:
                                return None
                        return cycle
        return cycle

    # Fin
    ######################################################################

import graph_examples
examples = graph_examples.Examples(Graph)
