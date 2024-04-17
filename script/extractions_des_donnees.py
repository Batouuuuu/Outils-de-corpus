## L'idée est de récuppérer des questions réponses sur ce forum 
## https://www.forumconstruire.com/construire/topic-474537-meilleur-protection-anti-rouille.php#6365329 

## Méthode :
## il faudrait sur la page principale trouver un moyen de parcourir les différents sujets
## on récupère les liens et on les extrait par exemple 
## comme il y'a beaucoup de réponses sur certaines questions il faudrait trouver un moyen de ne récuppérer que la meilleure réponse


from pathlib import Path
from typing import List, Set
import requests
from bs4 import BeautifulSoup
from datastructures import Page
import csv



def extraction_liens_forum(page_accueil : str | Path)-> Set[str]:
    """Extrait les différents liens d'ouverture d'une discussion que l'on retrouve sur la 
    page principale du forum et les sauvegardes"""
    
    liste_url = set() ## je ne sais pas pourquoi j'avais des doublons j'ai donc tout stocké dans un set
    URL = requests.get(page_accueil) 
    ##retirer les pubs
    liens_spam = ["https://www.forumconstruire.com/construire/devis-0-66-devis_renovation.php","https://achat.forumconstruire.com/vente-privee/"]
    soup = BeautifulSoup(URL.content, "html.parser")
    for lien in soup.find_all('a', class_='nounder'):
        url = lien.get('href')
        if url not in liens_spam:
            liste_url.add(url)

    return liste_url


def sauvegardes_liens(chemin_fichier : str | Path ,liste_urls : List[str])-> None:
    """Sauvegardes des URLs"""

    with open(chemin_fichier, "w") as fichier:
        fichier.write(str(liste_urls))


def ouverture_liens(liste_url : List[str]) -> List[BeautifulSoup]:
    """Ouvre les différents liens des discussions du forums, prends tout leur contenu, balisage... et les stocke dans une liste"""

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


def url_meilleurs_reponse(liste_url : Set[str]) -> List[str]:
    """Récupération de l'URL de la meilleure réponse et ajout dans une liste"""
    
    url_meilleurs_reponse = []
    print(len(liste_url))
    for lien in liste_url:
        response = requests.get(lien)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        div_tag = soup.find('div', class_='rectangle_gris ultra_padding')
        
        if div_tag:
            a_tag = div_tag.find('a')
            
            if a_tag:
                str_base = 'https://www.forumconstruire.com/'
                link = a_tag.get('href')
                lien_complet = str_base + link  ## concaténation on ajoute https car le lien est un chemin relatif
                url_meilleurs_reponse.append(lien_complet)
                
    return url_meilleurs_reponse



def recuperation_meilleure_reponse(liste_URL_reponse : List[str]):
    """Parcours l'URL où se trouve la meilleure réponse et récuppère la réponse avec le plus de likes"""
    

    comments_likes = []
    liste_meilleure_reponse = []
    print(len(liste_URL_reponse))
    for lien in liste_URL_reponse:
        print(lien)
        response = requests.get(lien)
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)
        like_divs = soup.find_all('div', class_='post_ilike touch_links')

        ## parcours de tous les commentaires et de leur nombre de like et ajout dans un tuple
        nombre_like = 0
        meilleure_reponse = ""
        for div in like_divs:
            like_count = int(div.find('span', class_='like_text').text.strip())
            comment_text = div.find_previous('div', class_='postsimple_message_cell').get_text(separator=" ", strip=True)
            tuple = (like_count, comment_text)
            comments_likes.append(tuple)
            # print(comments_likes)
    
            ##récupération du commentaire avec le plus de like 
            if like_count > nombre_like:
                nombre_like = like_count
                meilleure_reponse = comment_text
        liste_meilleure_reponse.append(meilleure_reponse)

    return liste_meilleure_reponse



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

    soup_liste = ouverture_liens(resultats_extraction)

    reponses_URL = url_meilleurs_reponse(resultats_extraction)
    test = recuperation_meilleure_reponse(reponses_URL)
    print(test)


    # sauvegardes_questions("../data/raw/questions.txt", questions)
    # ecriture_resultat_tsv('../data/dataset/dataset.csv',questions)
    # sauvegardes_liens("../data/raw/liens.txt", resultats_extraction)

if __name__ == "__main__":
    main()

