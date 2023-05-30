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

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bd99d756b40f0474676be6e6c593d4d3", "grade": false, "grade_id": "cell-f831ac926c595e4c", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "slide"}}

# [Parcours en largeur](https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_largeur) et calcul de distance

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "947b25e62854e71e22de6946a4d80239", "grade": false, "grade_id": "cell-05263ea2cabe0edb", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "fragment"}}

Dans cette feuille, nous raffinons l'algorithme de parcours de graphe
vu précédemment pour calculer des *distances simples* entre sommets
d'un graphe, ne tenant pas compte des poids des arêtes. Nous suivons
la même démarche que pour notre premier algorithme: invariants, test
sur des exemples, visualisation, complexité, preuve de correction.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "23c0034b2e510f1f1a3400c99b89714c", "grade": false, "grade_id": "cell-214af97aa4f0777b", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Définition** *distance simple* dans un graphe

La *distance* entre deux sommets $u$ et $v$ d'un graphe $G$ est le
plus petit entier $l$ tel qu'il existe un chemin avec $l$ arêtes
allant de $u$ à $v$. S'il n'y a pas de tel chemin, alors la distance
est $\infty$.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "bfa7b695e373cb1d5d66936307ce3b26", "grade": false, "grade_id": "cell-a29ce09f98694e4c", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice**

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "e9f25ef2a01d4b4c19eb7f995dae0d2f", "grade": false, "grade_id": "cell-5c625fc342cbb86c", "locked": true, "schema_version": 3, "solution": false, "task": false}, "slideshow": {"slide_type": "fragment"}}

1. Complétez la fonction suivante qui implante un parcours en largeur,
   en vous laissant guider par les invariants fournis:

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 3753a0f4df73daed96c9bd04d7e1f749
  grade: false
  grade_id: cell-fa2ebcc093dd410e
  locked: true
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: fragment
---
from graph import Graph, Node
from typing import Dict
```

```{code-cell} ipython3
from queue import SimpleQueue
```

```{code-cell} ipython3
test = SimpleQueue()
test.put('A')
if not test.empty():
    print("true")
```

```{code-cell} ipython3
---
code_folding: []
deletable: false
nbgrader:
  cell_type: code
  checksum: b2e6ad4af2509060a04d50ec2721292c
  grade: false
  grade_id: cell-fa2ebcc093dd410f
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: fragment
---
def parcours_en_largeur(G: Graph, u: Node) -> Dict[Node, int]:
    """
    INPUT:
    - 'G' - un graphe
    - 'u' - un sommet du graphe
    
    OUTPUT: un dictionnaire associant à chaque sommet `v` accessible depuis `u` sa distance depuis `u`
    """
    distances = {u: 0} # L'ensemble des sommets déjà rencontrés
    todo      = SimpleQueue()    # Une file de sommets à traiter
    todo.put(u)
    
    while not todo.empty():
        # Invariants:
        # - Si `v` est dans `distances`, alors il y a un chemin de `u` à `v`,
        #   et distances[v] contient la distance de `u` à `v`;
        # - Si `v` est dans `distances` et pas dans `todo`
        #   alors tous les voisins de `v` sont dans `distances`
        v = todo.get()
        for w in G.neighbors(v):
            if w not in distances:
                distances.update({w: 1+distances[v]})
                todo.put(w)
    return distances
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "cc1331bda55887175f90dc644c237d87", "grade": false, "grade_id": "cell-5deaa43c0e1f7147", "locked": true, "schema_version": 3, "solution": false, "task": false}}

2. Testez que votre fonction est correcte sur les exemples suivants.
   Si elle ne l'est pas, utilisez la question suivante pour déboguer!

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 951cbf527b66f2f1e2ef4c4dc627a817
  grade: false
  grade_id: cell-f22a5fce9c1128ba
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from graph import Graph, examples
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 7480702ba4ed85933fb8758081ab2ee1
  grade: false
  grade_id: cell-f22a5fce9c1128bb
  locked: true
  schema_version: 3
  solution: false
  task: false
---
C3 = examples.C3()
C3.edges()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 93935616489bffbe57b12b2d7dd6a04a
  grade: true
  grade_id: cell-e31ac5a2ec1ca694
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert parcours_en_largeur(C3, 0) == {0: 0, 1: 1, 2: 2}
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: c67e08465d3ad8bd8bf9e16433708f63
  grade: false
  grade_id: cell-f22a5fce9c1128bd
  locked: true
  schema_version: 3
  solution: false
  task: false
---
T3 = examples.T3()
T3.edges()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: b099bafd3e1b5c19579a359b2d30902c
  grade: true
  grade_id: cell-2a1fe26cce698ead
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert parcours_en_largeur(T3, 0) == {0: 0, 1: 1, 2: 1}
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 599bf832c16be88d6e1ac088b61f273b
  grade: false
  grade_id: cell-f61de6336f6d75cc
  locked: true
  schema_version: 3
  solution: false
  task: false
---
from graph import examples
G = examples.parcours_directed()
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 8d68f3d8d7ab81f16f43042b4251b89c
  grade: true
  grade_id: cell-8d83da87d56c871c
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert parcours_en_largeur(G, "H") == {'H': 0, 'F': 1, 'G': 2}
```

```{code-cell} ipython3
---
deletable: false
editable: false
nbgrader:
  cell_type: code
  checksum: 201a810f58277d5efc93b9c5a73d9e27
  grade: true
  grade_id: cell-1cefa7a59eae7cc6
  locked: true
  points: 1
  schema_version: 3
  solution: false
  task: false
---
assert parcours_en_largeur(G, "A") == {'A': 0, 'B': 1, 'G': 1, 'F': 1, 'C': 2, 'H': 2, 'D': 3}
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "af4b7c8f06f293aac77397ac6020a833", "grade": false, "grade_id": "cell-ae29bebcfa0eefba", "locked": true, "schema_version": 3, "solution": false, "task": false}}

3. Instrumentez votre code comme dans la feuille précédente pour visualiser son exécution

```{code-cell} ipython3
import copy
```

```{code-cell} ipython3
def parcours_en_largeur_visualisation(G: Graph, u: Node) -> Dict[Node, int]:
    """
    INPUT:
    - 'G' - un graphe
    - 'u' - un sommet du graphe
    
    OUTPUT: un dictionnaire associant à chaque sommet `v` accessible depuis `u` sa distance depuis `u`
    """
    distances = {u: 0} # L'ensemble des sommets déjà rencontrés
    todo      = [u]    # Une liste de sommets à traiter
    
    # Observation des variables locales
    player.player.reset(copy.deepcopy(locals()))
    
    while todo:
        # Invariants:
        # - Si `v` est dans `distances`, alors il y a un chemin de `u` à `v`,
        #   et distances[v] contient la distance de `u` à `v`;
        # - Si `v` est dans `distances` et pas dans `todo`
        #   alors tous les voisins de `v` sont dans `distances`
        
        
        # Comme je ne peux pas faire une deepcopy sur SimpleQueue j'utilise une liste
        # pour représenter une FIFO et j'utilise cette fonction qui est en O(n) pour
        # retirer un élément de la file, sa complexité est similaire à celle d'un
        # slice sur la liste sans le premier element
        v = todo.pop(0)
        # Observation des variables locales
        player.set_value(copy.deepcopy(locals()))
        for w in G.neighbors(v):
            if w not in distances:
                distances.update({w: 1+distances[v]})
                todo.append(w)
                # Observation des variables locales
                player.set_value(copy.deepcopy(locals()))
        v = None
        # Observation des variables locales
        player.set_value(copy.deepcopy(locals()))
    return distances
```

```{code-cell} ipython3
import graph_algorithm_player
variables = [{'name': 'G',      'type': 'graph' },
             {'name': 'distances', 'type': 'nodes', 'color': 'green',  'display': True},
             {'name': 'todo',   'type': 'nodes', 'color': 'red',    'display': True},
             {'name': 'v',      'type': 'node',  'color': 'yellow', 'display': True}]
player = graph_algorithm_player.GraphAlgorithmPlayer(variables=variables)
player
```

```{code-cell} ipython3
parcours_en_largeur_visualisation(G, "A")
```

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "4a54b3dff3906ba080e83120f4df2c48", "grade": false, "grade_id": "cell-c825b936675348a7", "locked": true, "schema_version": 3, "solution": false, "task": false}}

**Exercice** Complexité

Donner une borne de complexité pour l'algorithme `parcours_en_largeur`.

Note: pour simplifier, nous avons utilisé une liste pour `todo`. Pour
avoir une bonne complexité, il faudrait utiliser une *file* (FIFO),
typiquement implantée au moyen d'une liste chaînée et non un tableau
comme dans les listes Python. Voir par exemple `queue.SimpleQueue`.

+++

**Réponse**:  

*Modèle de compléxité:*  
On note :  
$n$ le nombre de sommets  
$m$ le nombre d'arêtes  
Les opérations élémentaires unitaires :  
- L'operation update() sur un dictionnaire et accès avec [] est généralement en $O(1)$ (sauf cas particulier avec beaucoup de collisions).
- La vérification si un élement est dans un dictionnaire est en $O(1)$
- L'opération put() sur une SimpleQueue append() sur une liste est en $O(1)$
- L'opération get() sur une SimpleQueue pop() sur une liste est en $O(1)$
- L'opération neighbors -dans la classe graph que j'ai implémentée- qui récupère tous les voisins d'un sommet a un coût constant (donc $O(1)$).  

De manière générale, tous les sommets dans la composante connexe du sommet initial passent exactement une fois dans `todo`, donc l'opération `neighbors` est appelée aussi exactement une fois sur chaque sommet, et on peut avoir au maximum $n$ sommets dans la composante connexe.  
La boucle `for`, quant à elle, n'est pas exécutée tout le temps grâce à la condition `if w not in distances`, dans le pire des cas, la boucle `for` est exécuté $m$ fois durant toute l'exécution de l'algorithme.  
On conclut que cet algorithme est d'un coût de $n+m$, donc il a une complexité de $O(n+m)$.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "2d3be46d5a5cbd96f7ba617453e3cda7", "grade": false, "grade_id": "cell-f3846db56cd75ff8", "locked": true, "schema_version": 3, "solution": false, "task": false}}

Bonus: chronométrez votre code sur des graphes de taille croissante
afin de tracer une courbe de complexité pratique et vérifier
empiriquement que votre code a la complexité voulue.

**Indication**: vous pouvez par exemple utiliser les outils
`time.time`, `%timit`, `timeit` ou
[bleachermark](https://github.com/miguelmarco/bleachermark) (note: ce
dernier n'est pas encore compatible Python 3).

+++

On peut bien voir que la compléxité en temps est de $O(n)$

```{code-cell} ipython3
import random
import time
import matplotlib.pyplot as plt

num_nodes = [8 * 2**x for x in range(10)]
times = []

for i in num_nodes:
    nodes = list(range(i))
    edges = []
    for _ in range(i//2):
        edges.append((0, random.choice(nodes), random.randint(1,10)))
    for _ in range(2*i-i//2):
        l = random.sample(nodes, 2)
        c = random.randint(1, 10)
        edges.append((l[0], l[1], c))
    G = Graph(nodes, edges=edges, directed=True)
    start = time.time()
    parcours_en_largeur(G, 0)
    end = time.time()
    times.append(end-start)
    
plt.plot(num_nodes, times)
plt.show()
```

+++ {"deletable": false, "nbgrader": {"cell_type": "markdown", "checksum": "f870fd88ac1ea46cf34b92b4ae6e6023", "grade": true, "grade_id": "cell-4602f238ddb35643", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}}

**Exercice** Preuve de correction

**Réponse**  
Preuve par invariants de boucle.  
Les invariants :  
- Si `v` est dans `distances`, alors il y a un chemin de `u` à `v`, et `distances[v]` contient la distance de `u` à `v`
- Si `v` est dans `distances` et pas dans `todo` alors tous les voisins de `v` sont dans `distances`

1. A l'initialisation, `distances = {u: 0}` et `todo = [u]`. Il y a un chemin entre `u` et `u` et `distances[u]`=0 (premier invariant respecté). Il n'y a pas d'élément dans `distances` qui n'est pas dans `todo` (le deuxième invariant est aussi respecté).
2. Supposons qu'au début de la nième itération, les invariants sont respectés. on retire $z$ de `todo` (donc $z$ est déjà dans `distances` et comme les invariants sont respectés donc il y a un chemin de `u` à $z$ de distance `distance[z]`).  
    On mets $voisins(z)$ qui ne sont pas déjà dans `distances` dans `distances` avec une distance de `1+distances[z]` et dans `todo`. Comme $z$ est dans `distances` et pas dans `todo` et que tous ses voisins $voisins(z)$ sont maintenant dans `marked` donc le deuxième invariant est respecté.  
    Etant donné qu'il y a un chemin entre `u` et $z$ donc il y a un chemin entre `u` et tous les nouveaux sommets $voisins(z)$ insérés dans `distances` et ce chemin = `1+distance[z]`, le premier invariant est alors respecté.  
    Par conséquent, les invariants sont toujours respectés à la fin de la nième itération.
3. Si les invariants sont respectés à la fin de l'itération n alors ils le sont au début de l'itération n+1. Par récurrence, les invariants sont respectés au début et la fin de l'itération n, quelque soit n le numéro de l'itération.
4. On veut montrer que s'il y a un chemin de `u` à `v`, alors `v` est dans `distances` et la distance de `u` à `v` est dans `distance[v]`.
    Si L'algorithme s'arrête lorsque `todo` est vide et que tous les voisins du dernier élément retiré de `todo` sont déjà dans `distances`. Par récurrence, les invariants sont respectés à la fin de cette dernière itération.  
    
    Par conséquent,  
    **(1)** $\forall v, v \in distances \implies voisins(v) \in distances$ (car $todo=\emptyset$ et l'invariant 2 est respecté)
    
    et,  
    **(2)** $\forall v, v \in distances \implies \exists chemin(u,v) \land distance(u,v) = distances[v]$ (invariant 1).  
    
    Supposons que $\exists chemin(u,v) = (u, s1, s2, ... , sn, v)$.  
    Comme $u \in distances$ et $s1 \in voisins(u)$ alors $s1 \in distances \land distance(u,s1) = distances[s1] (=1)$ (en utilisant **(1)**).  
    Comme $s1 \in distances$ et $s2 \in voisins(s1)$ alors $s2 \in distances \land distance(u,s2) = distances[s2] (=distance[s1]+1)$ (en utilisant **(1)**).  
    ...  
    Et ainsi de suite jusqu'à $sn \in distances$ et $v \in voisins(sn)$ alors $v \in distances \land distances(u,sn) = distance[sn]$ (en utilisant **(1)**).   
    **Conclusion**: s'il y a un chemin de `u` à `v`, alors `v` est dans `distances` et distance(u,v) est dans `distances[v]` à la fin de l'exécution de l'algorithme.

+++ {"deletable": false, "editable": false, "nbgrader": {"cell_type": "markdown", "checksum": "41e3521e65104239288bbab69f24f653", "grade": false, "grade_id": "cell-c1fde793cc0a2414", "locked": true, "schema_version": 3, "solution": false, "task": false}}

## Conclusion

Dans cette feuille, vous avez mené en toute autonomie l'implantation
et l'étude d'un autre parcours de graphe pour mettre en pratique tout
ce que nous avions vu dans la fiche précédente. Bravo!
