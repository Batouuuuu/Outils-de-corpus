"""Ce script récuppère une dizaine de questions qui proviennent d'une nouvelle page
du forum de bricolage : https://www.forumconstruire.com/construire/forum-51_start-250.php
ce script est similaire à celui d'extraction des données du forum mais cette fois-ci on ne récuppère
que la question et le sujet. Les questions seront ensuite posés à chatgpt 3.5 manuellement et ses réponses
seront écrites le csv (manuellement)"""

from extractions_des_donnees_forum import *
from datastructures import *
from pathlib import Path


    
def ecriture_resultat_tsv_complet(dataset_fichier : str | Path, data : Dataset) -> None: ##modification simple de la fonction qui existait deja mais ici on append au lieu d'écrire dans le tsv
    """Cette fonction écrit nos résultat dans le même fichier TSV """

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


# def ecriture_corpus(dataset : Dataset, chemin_fichier : str)-> None:
#     """Cette fonction récupère la question et la réponse du fichier tsv pour constituer le corpus de question réponse"""
#     with open(chemin_fichier, "w") as fichier:
#         for infos in dataset:
#             fichier.write(infos + '\n')


def main():

    
    liste_resultat = []
    resultats = extraction_liens_forum('https://www.forumconstruire.com/construire/forum-51_start-300.php')[:26]  # on ne prend que 26 liens d'une nouvelle page du forum    
    contenu_url = ouverture_liens(resultats)
    question = recuperation_question(contenu_url)
    sujet = recuperation_sujet_question(contenu_url)

    for i, (url, sujet, question) in enumerate(zip(resultats, sujet, question), start=1):
        alors = Page(
        id=i,
        lien=url,
        id_question=i,
        id_reponse=i,
        sujet=sujet,
        question=question,
        reponse=None, ## cette réponse sera mise manuellement dans le csv
        etiquette="CHATGPT"
        )
        liste_resultat.append(alors)

    dataset = Dataset(data=liste_resultat)
    ecriture_resultat_tsv_complet("../data/raw/test_question_chatgpt.tsv", dataset)

    

if __name__ == "__main__":
    main()

