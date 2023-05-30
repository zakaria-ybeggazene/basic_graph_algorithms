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

# Implantation

+++

## Rappels et exemples Python sur les dictionnaires et compréhensions

Suivez le tutoriel suivant: http://doc.sagemath.org/html/en/thematic_tutorials/tutorial-comprehensions.html

Puis analysez les exemples suivants:

```{code-cell} ipython3
l = [3,2,1,0]
[ i**2    for i in l ]
```

```{code-cell} ipython3
l = ["a", "z", "b"]
d = {l[i] : i for i in range(len(l))}
```

```{code-cell} ipython3
for v in d.keys():
    print(v)
```

```{code-cell} ipython3
[(v, 1) for v in l]
```

## Conversions

+++

**Exercice:**

Choisissez une des structure de données de graphes que l'on a vues
(liste d'arêtes, dictionnaire des voisins, dictionnaire d'arêtes,
matrice d'adjacence).

Implantez des fonctions Python `from_matrix`, `from_edges`,
`from_neighbor_dict`, `from_edge_dict`. Par exemple, la fonction
`from_matrix` prendra un graphe représenté par une matrice d'adjacence
et renverra le même graphe dans la structure de donnée que vous avez
choisi.

Testez ces fonctions sur les exemples de la fiche précédente.

```{code-cell} ipython3
# On suppose que lorsqu'il n'y a pas d'arête entre les sommets vi et vj, l'element ij de la matrice m est None
def from_matrix(m) -> list:
    assert isinstance(m, list), "matrix has to be of type list"
    if not m: return []
    assert all([isinstance(i, list) for i in m]), "all elements of matrix have to be of type list"
    l = len(m[0])
    assert all([len(i) == l for i in m]), "all list elements of matrix have to be of same length"
    return [(i,j,m[i][j]) for i in range(l) for j in range(l) if m[i][j] is not None]
```

```{code-cell} ipython3
M1 = [[None, None, None, None, None, None],
     [None, None, 1, 1, None, None],
     [None, None, None, None, 2, None],
     [None, None, None, None, 0, None],
     [None, None, None, None, None, 3],
     [None, None, None, None, None, None]]
from_matrix(M1)
```

```{code-cell} ipython3
def from_neighbor_dict(n) -> list:
    assert isinstance(n, dict), "neighbor dictionary has to be of type dict"
    assert all([isinstance(v, list) for _, v in n.items()]), "all values have to be of type list"
    assert all([isinstance(t, tuple) for _,v in n.items() for t in v]), "all elements inside values have to be of type tuple"
    return [(k,v,c) for k, l in n.items() for (v,c) in l]
```

```{code-cell} ipython3
DV1 = {1: [(2,1),(3,1)], 2: [(4,2)], 3: [(4,0)], 4: [(5,3)]}
from_neighbor_dict(DV1)
```

```{code-cell} ipython3
def from_edge_dict(e) -> list:
    assert isinstance(e, dict), "edge dictionary has to be of type dict"
    assert all([isinstance(t, tuple) for t,_ in e.items()]), "all keys have to be of type tuple"
    return [(u,v,c) for (u,v), c in e.items()]
```

```{code-cell} ipython3
DA1 = {
        (1,2): 1,
        (1,3): 1,
        (2,4): 2,
        (3,4): 0,
        (4,5): 3
    }
from_edge_dict(DA1)
```

## Une classe graphe

+++

Le fichier <a href="graph.py">graph.py</a> contient un squelette de classe pour
représenter des graphes. Votre mission pour la prochaine séance est de
compléter les méthodes non implantées. Le [rapport](Rapport.md)
contient des vérifications automatiques pour votre code. Utilisez le
au fur et à mesure pour suivre votre avancement et complétez le.
