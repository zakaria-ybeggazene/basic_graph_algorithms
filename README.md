---
jupytext:
  notebook_metadata_filter: rise
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
rise:
  auto_select: first
  autolaunch: false
  centered: false
  controls: false
  enable_chalkboard: true
  height: 100%
  margin: 0
  maxScale: 1
  minScale: 1
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"slideshow": {"slide_type": "slide"}}

# Algorithmique avancée

M1 Informatique pour la Science des Données, Université Paris-Saclay, Faculté d'Orsay

[Page web](http://nicolas.thiery.name/Enseignement/M1-ISD-AlgorithmiqueAvancee/),
[ENT eCampus](https://ecampus.paris-saclay.fr/course/view.php?id=63957)

+++ {"slideshow": {"slide_type": "fragment"}}

«L’objectif de ce cours est de fournir des outils et techniques
algorithmiques de pointe aux apprentis. Étude de l’algorithmique sur
les graphes (plus courts chemins, tri topologique, …), les techniques de
mémorisation, de programmation dynamique et de backtracking.
Présentation de la notion de flots et des algorithmes de calcul de flot
maximal. Enfin, les thèmes des algorithmes online et approchés seront
abordés.»

+++ {"slideshow": {"slide_type": "fragment"}}

## Enseignants

- [Florent Hivert](https://www.lri.fr/~hivert/)
- [Viviane Pons](https://www.lri.fr/~pons/en/)
- [Nicolas M. Thiéry](http://Nicolas.Thiery.name)

+++ {"slideshow": {"slide_type": "slide"}}

## Vue d'ensemble

+++

Les notions du cours seront abordées par la pratique, tout d'abord par
l'implantation de structures de données de graphes, puis leur
utilisation pour résoudre quatre problèmes.

+++ {"slideshow": {"slide_type": "fragment"}}

### Structures de données pour les graphes

+++ {"slideshow": {"slide_type": "subslide"}}

### Problème 1: Le chemin le plus rapide en métro de Montgallet à Billancourt ?

<center>

<img src="media/metro-paris.gif" width="50%">

</center>

+++ {"slideshow": {"slide_type": "subslide"}}

### Problème 2: [Rush Hour](http://www.thinkfun.com/products/rush-hour/)

La voiture rouge est coincée dans un embouteillage; comment déplacer les véhicules pour la faire sortir?
Ci-dessous le défi 1. Saurez-vous faire résoudre par l'ordinateur le défi 40 en un nombre minimum du coups?

<center>

<img src="media/rush_hour.gif" width="30%">

</center>

+++ {"slideshow": {"slide_type": "subslide"}}

### Problème 3: Faire passer le maximum de courant

<center>

<img src="media/reseau-electrique.png" width="50%">

</center>

+++ {"slideshow": {"slide_type": "subslide"}}

### Problème 4: Fabriquer et résoudre des labyrinthes

<center>

<img src="media/labyrinthe.png" width="50%">

</center>

+++ {"slideshow": {"slide_type": "slide"}}

## Planning

+++ {"slideshow": {"slide_type": "-"}}

3 semaines avec 3h + 3h: Cours + TD + TP intégré

+++ {"slideshow": {"slide_type": "fragment"}}

### Graphes: structures de données, terminologie, plus courts chemins (Nicolas)

- 2022-03-15 mar. 13:30-16:45
- 2022-03-18 ven. 13:30-16:45

+++ {"slideshow": {"slide_type": "fragment"}}

### Réseaux et flots (Nicolas)

- 2022-03-29 mar. 13:30-16:45
- 2022-04-01 ven. 13:30-16:45

+++ {"slideshow": {"slide_type": "fragment"}}

### Arbres couvrants (Florent)

- 2022-05-10 mar. 13:30-16:45
- 2022-05-12 jeu. 13:30-16:45

<!--
Tri topologique, ordonnancement simple (UET, 1 ou infinté processeurs)

Arbre, labyrithes, arbre couvrant de poids minimal algos Kruskal puis Prim.

Réseaux: Dijkstra, flots, Ford-Fulkerson, ...

Article de Mathieu Gay Paquet
!-->

+++ {"slideshow": {"slide_type": "slide"}}

### Modalités d'évaluation (à mettre à jour)

L'évaluation se fera sur les rendus de TP (CC), ainsi que sur un examen (ET1 / ET2)

Session 1 : 1/3 CC + 2/3 ET1

Session 2 : 1/3 CC + 2/3 ET2

+++ {"slideshow": {"slide_type": "fragment"}}

### Annales

- <a href="../2017-2018/exam-correction.pdf">Examen 2017-2018, avec correction</a>

+++ {"slideshow": {"slide_type": "slide"}}

## Environnement de travail

- Language de programmation: Python 3
- Environnement interactif: [Jupyter](https://jupyter.org) + networkx + matplotlib + ...

+++ {"slideshow": {"slide_type": "fragment"}}

Dans cette section, nous expliquons:
- Comment accéder aux logiciels requis
- Comment télécharger et déposer vos devoirs

Les instructions font l'hypothèse que vous travaillerez pour ce cours
dans votre répertoire `~/M1-ISD/AlgorithmiqueAvancee`. Vous pouvez
choisir un autre nom.

+++ {"slideshow": {"slide_type": "subslide"}}

### Utilisation des logiciels en ligne

L'université Paris-Saclay mets à votre disposition un service
[JupyterHub@Paris-Saclay](https://jupyterhub.ijclab.in2p3.fr/) sur
lequel sont installés tous les logiciels requis. Vous pouvez vous
identifier avec vos identifiants usuels de l'université (Adonis).

Il est aussi possible d'utiliser un des nombreux services Jupyter en
ligne tels [CoCalc](http://cocalc.com); ce dernier ne gère pas `bqplot`
cependant.

Alternativement, vous pouvez installer les logiciels sur votre machine
et travailler en local.

+++ {"slideshow": {"slide_type": "subslide"}}

### Installation de l'environnement de travail

Ce cours utilise Python, Jupyter et quelques bibliothèques classiques
(voir le fichier <a href="environment.yml">environment.yml</a>), ainsi
que quelques paquets Python plus ou moins maison.

+++ {"slideshow": {"slide_type": "fragment"}}

#### Avec miniconda (ou micromamba, ...)

- Téléchargez la «salle de TP virtuelle»:

      git clone https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/ComputerLab.git ~/M1-ISD/AlgorithmiqueAvancee

- Installer le gestionnaire de paquets [conda](https://conda.io):

  Voir son [guide d'installation](https://conda.io/docs/user-guide/install/index.html)

- Installez les logiciels requis:

	  cd ~/M1-ISD/AlgorithmiqueAvancee
      conda env create
	  ./postBuild
    
- Pour lancer Jupyter, taper:

      conda activate algo-avancee
      jupyter notebook

- Il peut arriver que la liste des logiciels soit mise à jour en cours
  de semestre. Dans ce cas, depuis le terminal ouvert sur le même
  dossier, taper:

      conda env update
      ./postBuild

+++ {"slideshow": {"slide_type": "subslide"}}

#### Avec pip

- Téléchargez la «salle de TP virtuelle»:

      git clone https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/ComputerLab.git ~/M1-ISD/AlgorithmiqueAvancee

- Assurez vous que vous avez toutes les bibliothèques requises (voir
  le fichier <a href="environment.yml">environment.yml</a>.

- Installez les paquets Python «maison»:

	  cd ~/M1-ISD/AlgorithmiqueAvancee
      pip install .
      ./postBuild

+++ {"slideshow": {"slide_type": "subslide"}}

#### Avec Docker

Une image docker du cours est fournie dans le
[Container Registry](https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/ComputerLab/container_registry)
du projet Gitlab du cours. Voici son identifiant:

    gitlab.dsi.universite-paris-saclay.fr:5005/m1infoisdalgorithmiqueavancee/computerlab/image:latest

+++ {"slideshow": {"slide_type": "slide"}}

### Téléchargement et dépôt des TPs

Les sujets sont donnés sous forme de dépôt git sur
https://gitlab.dsi.universite-paris-saclay.fr . Vous utiliserez git pour le télécharger et
le déposer sous la forme d'un fork. La correction se fera en partie
automatiquement par intégration continue. Il y a un script pour
automatiser le processus.

+++ {"slideshow": {"slide_type": "subslide"}}

#### Mise en place la première fois

+++ {"slideshow": {"slide_type": "subslide"}}

##### Activation compte GitLab Paris-Saclay

- Connectez vous à https://gitlab.dsi.universite-paris-saclay.fr
- Cliquez sur le boutton Sign-In en haut à droite pour vous authentifier avec vos identifiants de l'université (Adonis). Ils sont de la forme`Prenom.Nom`.

+++ {"slideshow": {"slide_type": "subslide"}}

##### Téléchargement de la «salle de TP virtuelle»

    git clone https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/ComputerLab.git ~/M1-ISD/AlgorithmiqueAvancee

Note: nous supposerons dans la documentation ci-dessous que vous avez
utilisé le nom de répertoire `~/M1-ISD/AlgorithmiqueAvancee/`. Vous
pouvez en utiliser un autre en adaptant les instructions.

+++ {"slideshow": {"slide_type": "subslide"}}

#### Téléchargement et dépôt des TPs avec travo

L'environnement de cours fournit un script qui automatise le
téléchargement et le dépôt de votre travail. Consultez sa
documentation avec:

	cd ~/M1-ISD/AlgorithmiqueAvancee
    ./course.py

Voir ci-dessous sur ce que cela fait, et comment faire pareil
à la main, si vous le souhaitez.

+++ {"slideshow": {"slide_type": "fragment"}}

#### Travail sur le TP

Ouvrez les feuilles Jupyter et suivez les instructions dans les
feuilles successives `README.md`, `00-*.md`, `01-*.md`, ... ainsi que
`Rapport.md`.

+++ {"slideshow": {"slide_type": "fragment"}}

#### Dépôt de votre travail

Consultez la documentation comme ci-dessus!

Vous pouvez déposer votre travail aussi souvent que vous le
souhaitez. Seule la dernière version disponible au moment de la
correction sera prise en compte.

+++ {"slideshow": {"slide_type": "fragment"}}

#### Consultation des résultats des tests automatiques

Vous pouvez consulter les résultats des tests automatiques en navigant
sur votre «fork» du dépôt:

    https://gitlab.dsi.universite-paris-saclay.fr/prenom.nom/<TP>

puis barre de menu de gauche -> `CI` -> `Pipelines` -> Badge `failed`
ou `passed` -> `test`. Le badge devrait être à `passed` dans tous les
cas. Vous pouvez alors consulter les feuilles de travail corrigées en
ouvrant `feedback/<...>.html` dans les artefacts (`Browse`). Le
navigateur vous donnera une alerte de certificat que vous pouvez -- à
titre exceptionnel -- ignorer.

+++ {"slideshow": {"slide_type": "subslide"}}

### Alternative: téléchargement et dépôt des TPs à la main

- Ouvrez le dépôt git de la séance du jour dans votre navigateur:

  https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/2020-2021/<TP>
  
  Par exemple:

  https://gitlab.dsi.universite-paris-saclay.fr/M1InfoISDAlgorithmiqueAvancee/2020-2021/1-StructuresDeDonnees

- Faites une copie personnelle du dépôt avec le bouton `Fork`
- Permettre aux enseignants d'accéder à votre dépôt: ajouter <!--Viviane
  Pons,!--> Florent Hivert et Nicolas Thiéry comme membres du projet,
  avec rôle «Mainteneurs» (`Settings` -> `Members`).
- Bonus:
  - Renommer le dépôt obtenu pour ajouter un préfixe précisant le cours
  - Basculez la visibilité de votre dépôt en privé (`Settings` ->
    `General` -> `Permissions`).

- Copiez l'adresse du dépôt (à droite du bouton `Fork`); elle devrait être de la forme

    `https://gitlab.dsi.universite-paris-saclay.fr/<prenom.nom>/<TP>`

- Téléchargez votre copie personnelle:

  Dans le terminal:

      cd ~/M1-ISD/AlgorithmiqueAvancee
      git clone https://...

  où https://... est l'adresse que vous avez copiée.

+++ {"slideshow": {"slide_type": "subslide"}}

#### Configurer git

Lancez les commandes suivantes dans le terminal après y avoir mis
respectivement votre mail et votre nom:

    git config --global user.email "prenom.nom@universite-paris-saclay.fr"
    git config --global user.name "Prénom Nom"

+++ {"slideshow": {"slide_type": "subslide"}}

#### Dépôt de votre travail

Pour déposer votre travail:

     git commit -m "Travail" .
     git push

Cela vous demandera vos identifiants et login Adonis.
