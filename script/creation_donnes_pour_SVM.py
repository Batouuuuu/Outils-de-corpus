""" (je préviens, script long a exécuté) Ce script va permettre de constituer un tsv qui nous permettra d'entrainer notre classifieur SVM. Il s'agit de la seule alternative
que j'ai trouvé pour juger de la pertinence d'une réponse. Nous allons parcourir plusieurs pages du blog et récuppérer des 
questions et des réponses aléatoires puis nous récupérerons des questions et les bonnes réponses, ainsi nous auront la pertinence
OUI ou NON qui nous permettra de créer notre classification binaire utile pour le SVM """

import random
from extractions_des_donnees_forum import *
from datastructures import * 

def recuperation_reponse_aleatoire(liste_reponses: List[str]) -> List[str]:
    """Récupère plusieurs réponses au hasard parmi la liste de réponses fournies."""
    
    reponses_aleatoires = set()

    for _ in range(len(liste_reponses)):
        reponse_aleatoire = random.choice(liste_reponses)
        reponses_aleatoires.add(reponse_aleatoire)  

    resultat_mauvaises_reponses = list(reponses_aleatoires)
    return resultat_mauvaises_reponses



def ecriture_resultats(dataset_fichier : str | Path, data : Liste_Reponses_SVM) -> None:
    """Cette fonction écrit nos résultat dans un fichier TSV"""

    with open(dataset_fichier, "w", newline='', encoding='UTF-8') as resultats_tsv:
        ecriture = csv.writer(resultats_tsv, delimiter="\t")
        ecriture.writerow(["Pertinence","Question", "Reponse"])
        
        for mauvaise_reponse in data.data:
            ecriture.writerow([
                mauvaise_reponse.pertinence,
                mauvaise_reponse.question,
                mauvaise_reponse.reponse,  
            ])

def main():
    ##Ce main est différent on va donner plusieurs url de pages du forums afin d'avoir pleins de données pour pourvoir avoir beaucoup de cas pour notre classifieurs svm et mieux l'entrainer
    
    pages_urls = [
    "https://www.forumconstruire.com/construire/forum-51_start-950.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1000.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1050.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1100.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1150.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1200.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1250.php",
    "https://www.forumconstruire.com/construire/forum-51_start-1300.php"
    ]

    liste = []
    ## on va boucler  à chaque fois pour les différentes url

    for page_url in pages_urls:
        resultats_extraction = extraction_liens_forum(page_url)
        soup_liste = ouverture_liens(resultats_extraction)
        questions = recuperation_question(soup_liste)
        reponses_URL = url_meilleurs_reponse(resultats_extraction)
        reponses = recuperation_meilleure_reponse(reponses_URL)
        reponse_aleatoire = recuperation_reponse_aleatoire(reponses)
        #print(reponse_aleatoire)

        ## ici on récupère avec les réponses aléatoires
        for _ , (question, reponse)  in enumerate(zip(questions, reponse_aleatoire), start=1):
            extraction = Reponse_SVM(
                pertinence="NON",
                question = question,
                reponse = reponse,
                
            )
            liste.append(extraction)
        
        # ## même principe mais cette fois c'est avec les bonnes réponses
        for _ , (question, reponse)  in enumerate(zip(questions, reponses), start=1): 
            extraction = Reponse_SVM(
                pertinence="OUI",
                question = question,
                reponse = reponse,
                
            )
            liste.append(extraction)
    
    dataset = Liste_Reponses_SVM(data=liste)
    ecriture_resultats('../data/training/donnees_SVM.tsv', dataset)

if __name__ == "__main__":
    main()
