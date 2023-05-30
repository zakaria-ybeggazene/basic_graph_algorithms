---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "a4fb7dbd00101f46e7d957b519779f48", "grade": false, "grade_id": "cell-916f6e1be3f587ad", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": true}, "slideshow": {"slide_type": "subslide"}}

# [Parcours en profondeur](https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_profondeur)

Dans cette feuille, nous étudions ce qu'il advient lorsque l'on
remplace la file `todo` de notre algorithme de parcours en largeur par
une pile.

Implantez l'algorithme de parcours en profondeur par une fonction
récursive comme sur la page wikipedia, et comparez les résultats des
deux algorithmes sur quelques exemples bien choisis.

```{code-cell} ipython3
from graph import Graph, Node
from typing import Dict, Any
```

Version iterative

```{code-cell} ipython3
def parcours_en_profondeur(G: Graph, u: Node) -> Dict[Node, int]:
    """
    INPUT:
    - 'G' - un graphe
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
        for w in G.neighbors(v):
            if w not in distances:
                distances.update({w: 1+distances[v]})
                todo.append(w)
    return distances
```

Version récursive

```{code-cell} ipython3
def explorer(G: Graph, u: Node, distances: Dict[Any, int], cur_dist: int):
    distances.update({u: cur_dist})
    for w in G.neighbors(u):
        if w not in distances:
            explorer(G, w, distances, cur_dist+1)
    return distances
def parcours_en_profondeur_rec(G: Graph, u: Node) -> Dict[Node, int]:
    """
    INPUT:
    - 'G' - un graphe
    - 'u' - un sommet du graphe
    
    OUTPUT: un dictionnaire associant à chaque sommet `v` accessible depuis `u` sa distance depuis `u`
    """
    distances = {}
    return explorer(G, u, distances, 0)
```

```{code-cell} ipython3
from graph import Graph, examples
```

```{code-cell} ipython3
C3 = examples.C3()
C3.edges()
```

```{code-cell} ipython3
assert parcours_en_profondeur(C3, 0) == {0: 0, 1: 1, 2: 2}
assert parcours_en_profondeur_rec(C3, 0) == {0: 0, 1: 1, 2: 2}
```

Sur des graphes très profonds, la performance de la version récursive se dégrade de plus en plus. Et je n'ai pas trouvé comment faire une version tail-recursive pour éviter le débordement de pile d'appels. On préfèrera la version itérative.

```{code-cell} ipython3
import random
import time

num_nodes = [8 * 2**x for x in range(10)]

for i in num_nodes:
    nodes = list(range(i))
    edges = []
    for j in range(i):
        edges.append((j, j+1, random.randint(1,10)))
    G = Graph(nodes, edges=edges, directed=True)
    start = time.time()
    parcours_en_profondeur(G, 0)
    end = time.time()
    print(f"Time iterative version:{end-start}")
    start = time.time()
    parcours_en_profondeur_rec(G, 0)
    end = time.time()
    print(f"Time recursive version:{end-start}")
```
