from dataclasses import dataclass
from typing import List

@dataclass
class Page:
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
    data : List[Page]

@dataclass
class Reponse_SVM:
    question : str
    reponse : str
    pertinence : str


@dataclass
class Liste_Reponses_SVM:
    data : List[Reponse_SVM]

