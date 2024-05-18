"""Script qui contient nos datastructures"""

from dataclasses import dataclass
from typing import List

@dataclass
class Page:
    """
    Représente une page contenant des informations sur une question et une réponse.

    Attributs:
    id (int): L'identifiant unique de la page.
    lien (str): Le lien vers la page en ligne.
    id_question (int): L'identifiant unique de la question.
    id_reponse (int): L'identifiant unique de la réponse.
    sujet (str): Le sujet ou domaine de la question.
    question (str): Le texte de la question.
    reponse (str): Le texte de la réponse.
    etiquette (str): L'étiquette ou catégorie associée à la question et la réponse.
    """

    id : int
    lien : str
    id_question : int
    id_reponse : int
    sujet : str ## anciennement domaine a été remplacé pour le sujet de la question (les raisons sont expliquées dans le journal)
    question : str
    reponse : str
    etiquette : str

@dataclass
class Dataset:
    """
    Contient nos différentes données des objets Page.

    Attributs:
    data (List[Page]): La liste des objets Page.
    """

    data : List[Page]

@dataclass
class Reponse_SVM:
    """
    Représente une extraction des questions et réponses qui nous serviront dans l'entrainement de notre classifieur SVM.

    Attributs:
    question (str): Le texte de la question.
    reponse (str): Le texte de la réponse.
    pertinence (str): La pertinence de la réponse pour la question donnée soit OUI soit NON.
    """

    question : str
    reponse : str
    pertinence : str


@dataclass
class Liste_Reponses_SVM:
    """
    Contient nos différentes données des objets Reponse_SVM.

    Attributs:
    data (List[Reponse_SVM]): La liste des objets Reponse_SVM.
    """
     
    data : List[Reponse_SVM]

