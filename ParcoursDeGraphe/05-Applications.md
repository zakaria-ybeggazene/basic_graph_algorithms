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

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "e1ca35f96e5c4f104595b0ba48fda2ea", "grade": false, "grade_id": "cell-7fa94557a9528c30", "locked": true, "schema_version": 3, "solution": false, "task": false}}

# Applications

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "57d7bfa2939260a132e6db778d0921f4", "grade": false, "grade_id": "cell-0bf805f0964bb953", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Composantes connexes
Soit $G$ un graphe non orienté. La composante connexe d'un sommet $s$ de $G$ est l'ensemble des sommets atteignables depuis $s$ en suivant un chemin dans $G$.

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "c02bfb32f1b13a9c8f17fbf72bb42878", "grade": false, "grade_id": "cell-e6440dd43c4d8889", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice**
1. Décrire un algorithme pour calculer toutes les composantes connexes d'un graphe non orienté
2. (Bonus) Implanter cet algorithme et visualiser son exécution

+++

**Réponse**  
Pour distinguer les composantes connexes les unes des autres, chaque sommet se verra attribuer une couleur; deux sommets de même couleur seront dans la même composante.
On écrit la fonction CC_sommet(G,x,i) qui colorie la composante connexe d'un sommet x avec la couleur i :
```
colorier x avec i
pour tout sommet y successeur de x
  si y n'est pas colorié faire CC_sommet(G,y,i)
```

Ensuite on écrit une fonction CC(G) qui colorie toutes les composantes connexes d'un graphe avec une couleur par composante :
```
tant que tous les sommets de G ne sont pas coloriés
  choisir un sommet x non colorié
  choisir une nouvelle couleur i
  CC_sommet(G,x,i)
```
Repose sur le parcours en profondeur.

```{code-cell} ipython3
from graph import Graph, Node
from typing import Dict

def parcours_en_profondeur(G: Graph, u: Node) -> Dict[Node, int]:
    """
    INPUT:
    - 'G' - un graphe
    - 'u' - un sommet du graphe
    
    OUTPUT: L'ensemble des sommets atteignables depuis `u`
    """
    CC = {u} # L'ensemble des sommets atteignables depuis u
    todo = [u]    # Une liste de sommets à traiter
    
    while todo:
        v = todo.pop()
        for w in G.neighbors(v):
            if w not in CC:
                CC.add(w)
                todo.append(w)
    return CC
```

```{code-cell} ipython3
from typing import Dict, Set
from graph import Graph, Node
def CC(G: Graph) -> Dict[int, Set[Node]]:
    """
    INPUT:
    - 'G' - un graphe
    
    OUTPUT: un dictionnaire contenant toutes les composantes connexes de G
    """
    CC = {} # Dictionnaire des composantes connexes
    todo = set(G.nodes())   # Ensemble des sommets pas encore coloriés
    i = 0
    while todo:
        u = todo.pop()
        CC[i] = parcours_en_profondeur(G, u)
        todo = todo - CC[i]
        i+=1
    return CC
```

```{code-cell} ipython3
from graph import examples
G = examples.undirected()
CC(G)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
G.show()
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "2c402bc596f9c6a3c36d6e43ddaa23ab", "grade": false, "grade_id": "cell-42d362e08da6e54f", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Généralisation

**Exercice**:

1. Généraliser la fonction `parcours` de la fiche [01-ParcoursDeGraphe.ipynb](01-ParcoursDeGraphe.ipynb) pour qu'elle prenne en argument la *fonction de voisinage* du graphe plutôt que le graphe lui-même.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: b23f06ee9c484e273b3bfcafe1278273
  grade: false
  grade_id: cell-203cbf9059dad7fa
  locked: false
  schema_version: 3
  solution: true
  task: false
---
from typing import Callable, Iterable, Set
from graph import Node

def parcours_fonction(voisins: Callable[[Node], Iterable[Node]], u: Node) -> Set[Node]:
    """
    INPUT:
    - `voisins`: une fonction telle que `voisins(v)` renvoie les voisins sortants de `v`
    - 'u' - un sommet du graphe
    
    OUTPUT: l'ensemble des sommets `v` de `G`
            tels qu'il existe un chemin de `u` à `v`
    """
    marked = {u} # L'ensemble des sommets déjà rencontrés
    todo   = {u} # L'ensemble des sommets déjà rencontrés, mais pas encore traités
    
    while todo:
        # Invariants:
        # - Si `v` est dans `marked`, alors il y a un chemin de `u` à `v`
        # - Si `v` est dans `marked` et pas dans `todo`
        #   alors tous les voisins de `v` sont dans dans `marked`
        v = todo.pop()
        for w in voisins(v):
            if w not in marked:
                marked.add(w)
                todo.add(w)
    return marked
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "fc7b0298a761ae8837b8a00c8d265498", "grade": false, "grade_id": "cell-035bdd195a5c981c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2. Testez votre fonction sur l'exemple suivant.  
   **Indication**: étant donné un graphe `G` tel que implanté précédément, la fonction `voisins` requise par `distance` peut être construite comme suit:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: 4eb6952971d7f60f6796159b9e94bafb
  grade: false
  grade_id: cell-8c06644285f181e9
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from graph import examples
G = examples.parcours_directed()
voisins = G.neighbors
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  checksum: 39c8e1a1631b46bbbab4d2018a148059
  grade: true
  grade_id: cell-c0385743a593b35c
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert parcours_fonction(voisins, 'D') == {'D', 'F', 'G', 'H'}
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "90330a5531918591dce76048c8906986", "grade": false, "grade_id": "cell-710d5a14b2c7464c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2. Reprenez de même tous les tests de la fiche 01 avec votre nouvelle fonction

```{code-cell} ipython3
H = examples.cours_1_reseau()
assert parcours_fonction(G.neighbors, "A") == {'A', 'B', 'C', 'D', 'F', 'G', 'H'}
```

```{code-cell} ipython3
assert parcours_fonction(G.neighbors, "B") == {'B', 'C', 'D', 'F', 'G', 'H'}
```

```{code-cell} ipython3
H = examples.cours_1_G()
assert sorted(parcours_fonction(H.neighbors, 3)) == [0, 1, 2, 3, 4, 5]
```

```{code-cell} ipython3
H = examples.disconnected()
assert sorted(parcours_fonction(H.neighbors, 1)) == [1, 2, 5]
assert sorted(parcours_fonction(H.neighbors, 3)) == [3, 4]
```

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "a6945c3deb4e4ca66369f2f53204b833", "grade": false, "grade_id": "cell-762972522930912c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Application: ensembles définis récursivement
De nombreux ensembles mathématiques sont définis en donnant quelques éléments initiaux, puis en applicant récursivement un processus permettant de produire de nouveaux éléments à partir d'éléments déjà présents. Par exemple, l'ensemble des entiers naturels est construit à partir de $0$ et de la fonction successeur $x \mapsto x+1$.

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "cbca65202ae74c22f9240f26e8dccf8b", "grade": false, "grade_id": "cell-2aa4625a03b106d8", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "subslide"}}

**Définition:**

Soit $E$ un ensemble, $R\subset E$ un sous ensemble fini, et $f$ une fonction associant à chaque élément de $E$ un sous-ensemble fini de $E$. L'ensemble $f$ défini récursivement par $R$ et $f$ est le plus petit sous-ensemble de $E$ contenant $R$ et *stable* par $f$: si $e\in F$ alors $f(e)\subset F$.

+++ {"deletable": false, "nbgrader": {"checksum": "5472bd08bf929ef92ffb952552f07562", "grade": true, "grade_id": "cell-d00c1b613f9e6da2", "locked": false, "points": 4, "schema_version": 3, "solution": true, "task": false}, "slideshow": {"slide_type": "subslide"}}

**Exercice**

Décrire les ensembles définis récursivement obtenus dans chacun des cas suivants:
- $E=\mathbb N$, $R=\{1\}$, $f(e) = \{ e + 2 \}$
  Réponse : $\{\forall n \in E, 2n+1\}$

- $E=\mathbb N$, $R=\{1\}$, $f(e) = \{ 2e, e+3 \}$
  Réponse : $\mathbb N - \{\forall n \in \mathbb N, 3n\}$

- $E$: listes, $R=\{()\}$, $f(u)$: rajouter $0$ ou $1$ à la fin du $u$
  Réponse : $\{\forall l \in E,\forall n \in l: n \in \{0,1\}\}$

- $E$: listes, $R=\{(1,2,3,2,1)\}$, $f(u)$: supprimer la première ou dernière lettre de $u$
  Réponse : $\{(1),(2),(3),(1,2),(2,1),(2,3),(3,2),(1,2,3),(2,3,2),(3,2,1),(1,2,3,2),(2,3,2,1),(1,2,3,2,1)\}$

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "c5b1ed41608ab4f65a516468bb0de780", "grade": false, "grade_id": "cell-87e84eed2d08ea7e", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "subslide"}}

**Exercice**

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "6d60ce38c045b0e89a94564e7d71ac90", "grade": false, "grade_id": "cell-08700a3e88cf3428", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Soit $C_n$ l'ensemble récursivement défini par:
- $R=\{ (\underbrace{1,1,\cdots,1}_n)\}$
- $f$ qui a une liste associe toute les listes obtenues en regroupant et sommant deux entrées consécutives<br>
Par exemple, $f((2,3,1,1)) = \{(5,1,1), (2,4,1), (2,3,2)\}$

+++ {"deletable": false, "nbgrader": {"checksum": "9a96022c9f2dfc2eb176015fee285b16", "grade": true, "grade_id": "cell-55b16a3d76390cbb", "locked": false, "points": 4, "schema_version": 3, "solution": true, "task": false}}

- Calculer à la main les **quatres** éléments de $C_3$, sans oublier $(3)$!
- Calculer avec la machine tous les éléments de $C_6$.
- Combien y en a t'il?

- Même chose pour $C_1,C_2,C_3,C_4,C_5$.
- Que conjecturez vous?
- Pouvez vous le prouver?

+++

**Réponse:**  
- $C_3=\{(1,1,1),(2,1),(1,2),(3)\}$
- Calcul des éléments de $C_6$ :

```{code-cell} ipython3
def C_n(R):
    C = R.copy()
    todo = R
    while todo:
        u = todo.pop()
        for i in range(len(u)-1):
            v = [k for k in u]
            v[i:i+2] = [v[i]+v[i+1]]
            t = tuple(v)
            if t not in C:
                todo.add(t)
                C.add(t)
    return C
```

```{code-cell} ipython3
R = {(1,1,1,1,1,1)}
C6 = C_n(R)
C6
```

- $C_6$ contient 32 éléments
- Même chose pours les autres ensembles :

```{code-cell} ipython3
C1 = C_n({(1,)})
print(f"C1: {C1} et len = {len(C1)}")
C2 = C_n({(1,1)})
print(f"C2: {C2} et len = {len(C2)}")
C3 = C_n({(1,1,1)})
print(f"C3: {C3} et len = {len(C3)}")
C4 = C_n({(1,1,1,1)})
print(f"C4: {C4} et len = {len(C4)}")
C5 = C_n({(1,1,1,1,1)})
print(f"C5: {C5} et len = {len(C5)}")
```

- On conjecture que $\forall n \in \mathbb N, |C_n| = 2^{n-1}$
- On le prouve par recurrence:

+++ {"deletable": false, "editable": false, "nbgrader": {"checksum": "3cae93e9b4d8f17083111e89058f309f", "grade": false, "grade_id": "cell-c619ca94679e9fbb", "locked": true, "schema_version": 3, "solution": false, "task": false}}

###### **Exercice** (bonus)
Une *permutation* est une liste d'entiers telle que, si $n$ est sa longueur, alors tous les entiers de $1$ à $n$ apparaissent exactement une fois. Décrire l'ensemble des permutations comme un ensemble énuméré. Utiliser cela pour lister toutes les permutations de longueur $n\leq 6$

```{code-cell} ipython3
---
deletable: false
nbgrader:
  checksum: 89063f64eacfefe6cbaa35413bbc1aab
  grade: true
  grade_id: cell-e75b5213a8b5e829
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
---

```
