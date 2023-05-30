#!/usr/bin/env python

from travo import GitLab
from travo.jupyter_course import JupyterCourse
from travo.script import main

forge = GitLab("https://gitlab.dsi.universite-paris-saclay.fr")
course = JupyterCourse(forge=forge,
                       path="M1InfoISDAlgorithmiqueAvancee",
                       name="M1 ISD - Algorithmique Avancée",
                       student_dir="./",
                       assignments_group_path="M1InfoISDAlgorithmiqueAvancee/2021-2022",
                       assignments_group_name="2020-2021",
                       script="./course.py",
                       expires_at="2023-07-31",
                       jobs_enabled_for_students=True,
                       )

usage = f"""Aide pour l'utilisation de la commande {course.script}
===============================================

Télécharger ou mettre à jour un TP ou un projet (ici pour le premier TP):

    {course.script} fetch 1-StructuresDeDonnees

Lancer le notebook Jupyter (inutile sur le service JupyterHub):

    {course.script} jupyter notebook

Soumettre son TP ou projet (ici pour le premier TP)

    {course.script} submit 1-StructuresDeDonnees

Télécharger le résultat de la correction automatique (ici le premier TP)

    {course.script} fetch_feedback 1-StructuresDeDonnees

Plus d'aide:

    {course.script} --help
"""


if __name__ == '__main__':
    main(course, usage)
