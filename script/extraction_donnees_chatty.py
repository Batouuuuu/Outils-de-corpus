"""Ce script récuppère une dizaine de questions qui proviennent d'une nouvelle page
du forum de bricolage : https://www.forumconstruire.com/construire/forum-51_start-250.php
ce script est similaire à celui d'extraction des données du forum mais cette fois-ci on ne récuppère
que la question et le sujet. Les questions seront ensuite posées à chatgpt 3.5 manuellement et ses réponses
seront écrites le csv (manuellement)"""

from extractions_des_donnees_forum import *
from datastructures import *
from pathlib import Path


    
def ecriture_resultat_tsv_complet(dataset_fichier : str | Path, data : Dataset) -> None: 
    ##modification simple de la fonction qui existait deja
    """
    Écrit les résultats dans le même fichier TSV.

    Cette fonction prend en entrée un chemin de fichier et un objet Dataset contenant des données structurées.
    Elle écrit ces données dans un fichier TSV avec les colonnes suivantes :
    ID, URL, Question_ID, Reponse_ID, Sujet, Question, Reponse, Etiquette.

    Parametres:
    dataset_fichier (str | Path): Le chemin du fichier où les résultats seront écrits.
    data (Dataset): Un objet Dataset contenant les données à écrire dans le fichier.

    Returns:
    None
    """

    with open(dataset_fichier, "w", newline='', encoding='UTF-8') as resultats_tsv:
        ecriture = csv.writer(resultats_tsv, delimiter="\t")

        for page in data.data:
            ecriture.writerow([
                page.id,
                page.lien,
                page.id_question,
                page.id_reponse,
                page.sujet,
                page.question,
                page.reponse,
                page.etiquette
            ])

def main():
    ##main similaire a celui qu'il y'a dans extractions_des_donnes_forums.py
    
    liste_resultat = []
    resultats = extraction_liens_forum('https://www.forumconstruire.com/construire/forum-51_start-300.php')[:26]  # on ne prend que 26 liens d'une nouvelle page du forum    
    contenu_url = ouverture_liens(resultats)
    question = recuperation_question(contenu_url)
    sujet = recuperation_sujet_question(contenu_url)

    ## même principe on va parcourir tous nos résultats zippés et les ajouter dans notre dataclass
    for i, (url, sujet, question) in enumerate(zip(resultats, sujet, question), start=1):
        extraction = Page(
        id=i,
        lien=url,
        id_question=i,
        id_reponse=i,
        sujet=sujet,
        question=question,
        reponse=None, ## cette réponse sera écrite par chatgpt et mise manuellement dans le csv
        etiquette="CHATGPT" ## réponse écrite par chagpt
        )
        liste_resultat.append(extraction)

    dataset = Dataset(data=liste_resultat)
    ecriture_resultat_tsv_complet("../data/raw/test_question_chatgpt.tsv", dataset)  ## écriture des résultats dans un tsv

    

if __name__ == "__main__":
    main()

