## L'idée est de récuppérer des questions réponses sur ce forum 
## https://www.forumconstruire.com/construire/topic-474537-meilleur-protection-anti-rouille.php#6365329 

## Méthode :
## il faudrait sur la page principale trouver un moyen de parcourir les différents sujets
## on récupère les liens et on les extrait par exemple 
## comme il y'a beaucoup de réponses sur certaines questions il faudrait trouver un moyen de ne récuppérer que la meilleure réponse


from pathlib import Path
from typing import List
import requests
from bs4 import BeautifulSoup
from datastructures import Page
import csv



def extraction_liens_forum(page_accueil : str | Path)-> List[str]:
    """Extrait les différents liens d'ouverture d'une discussion que l'on retrouve sur la 
    page principale du forum et les sauvegardes"""
    
    liste_url = []
    URL = requests.get(page_accueil) 
    # print(URL.content) 
    liens_spam = ["https://www.forumconstruire.com/construire/devis-0-66-devis_renovation.php","https://achat.forumconstruire.com/vente-privee/"]
    soup = BeautifulSoup(URL.content, "html.parser")
    for lien in soup.find_all('a', class_='nounder'):
        url = lien.get('href')
        if url not in liens_spam:
            liste_url.append(url)

    return liste_url


def sauvegardes_liens(chemin_fichier : str | Path ,liste_urls : List[str])-> None:
    """Sauvegardes des URLs"""

    with open(chemin_fichier, "w") as fichier:
        fichier.write(str(liste_urls))


def ouverture_liens(liste_url : List[str]) -> List[BeautifulSoup]:
    """Ouvre les différents liens des discussions du forums"""

    liste_soup = []
    for lien in liste_url:
        recuperation_sujet_dicussion = requests.get(lien)
        soup = BeautifulSoup(recuperation_sujet_dicussion.content, "html.parser", from_encoding="utf-8")
        liste_soup.append(soup)
    return liste_soup


def recuperation_question(soup_liste : List[BeautifulSoup]) -> List[str]:
    """Récupération et prétraitement des questions"""
    
    liste_question = []
    for numero,soup in enumerate(soup_liste):
        premier_message_bloc = soup.find("div", class_="first_message_bloc")
        if premier_message_bloc: ##des fois il peut ne pas y avoir de question
            question = premier_message_bloc.get_text(separator=" ", strip=True)
            # print(f"question numéro {numero }: {question}")
            liste_question.append(question)
    return liste_question


def sauvegardes_questions(chemin_fichier : str | Path, liste_question : List[str]) -> None:
    """sauvegardes des questions"""

    with open(chemin_fichier, "w", encoding='UTF8') as resultat:
        for numero,question in enumerate(liste_question):
            resultat.write(f"Question {numero}: {question}\n") 


def recuperation_meilleure_reponse(soup_liste : List[BeautifulSoup]) -> List[str]:
    """Récupération des meilleures réponses, 2 cas possibles : elle se trouve sur la même page, ou sur une
    autre page"""

    liste_reponse = []
    for soup in soup_liste:
        meilleure_reponse = soup.find("div", class_="post_resume_topic disnone")
        if meilleure_reponse: ##cas où la meilleure réponse se trouve sur la même page
            reponse = meilleure_reponse.get_text(separator=" ", strip=True) 
            liste_reponse.appden(reponse)
        else: #cas où la réponse se trouve sur une page différente du sujet
            meilleure_reponse = soup.find("div", class_="rectangle_gris ultra_padding")
            lien_rectangle = meilleure_reponse.find("a")
            if lien_rectangle:
                lien_rectangle_href = lien_rectangle.get("href")
                recuperation_lien_meilleure_reponse = requests.get(lien_rectangle_href)
                soup = BeautifulSoup(recuperation_lien_meilleure_reponse.content, "html.parser")
            
    return liste_reponse

def extraction_question_reponse_chatgpt():
    NotImplemented


def identification_chatgpt(): 
    NotImplemented


def ecriture_resultat_tsv(dataset_fichier : str | Path, questions : List[str]) -> None:
    """Cette fonction écrit tous nos résultat dans un csv"""

    with open(dataset_fichier, "w", newline='', encoding='UTF-8') as resultats_csv:
        ecriture = csv.writer(resultats_csv, delimiter=" ")
        ecriture.writerow(["question"])
        for question in questions:
            ecriture.writerow([question])


def main():

    resultats_extraction = extraction_liens_forum("https://www.forumconstruire.com/construire/forum-51.php")
    sauvegardes_liens("../data/raw/liens.txt", resultats_extraction)
    soup_liste = ouverture_liens(resultats_extraction)
    questions = recuperation_question(soup_liste)
    sauvegardes_questions("../data/raw/questions.txt", questions)
    ecriture_resultat_tsv('../data/dataset/dataset.csv',questions)
    # recuperation_meilleure_reponse(soup_liste)

if __name__ == "__main__":
    main()

