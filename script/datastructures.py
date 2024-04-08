from dataclasses import dataclass

@dataclass
class Page:
    id : int
    lien : str
    id_question : int
    id_reponse : int
    #bucket : ?
    domaine : str
    question : str
    reponse : str
    #etiquette : str

