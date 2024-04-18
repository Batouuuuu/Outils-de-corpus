from dataclasses import dataclass
from typing import List

@dataclass
class Page:
    id : int
    lien : str
    id_question : int
    id_reponse : int
    #bucket : ?
    sujet : str ## anciennement domaine a été remplacé pour le sujet de la question (les raisons sont expliquées dans le journal)
    question : str
    reponse : str
    etiquette : str

@dataclass
class Dataset:
    data : List[Page]

