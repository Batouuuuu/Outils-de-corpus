## l'idée est de récuppérer des questions réponses sur ce forum 
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



def extraction_liens_forum(page_accueil : str | Path)-> List[str]:
    """Extrait les différents liens d'ouverture d'une discussion que l'on retrouve sur la page principale du forum et les sauvegardes"""
    
    liste_url = []
    URL = requests.get(page_accueil) 
    # print(URL.content) 
    liens_spam = ["https://www.forumconstruire.com/construire/devis-0-66-devis_renovation.php","https://achat.forumconstruire.com/vente-privee/"]
    soup = BeautifulSoup(URL.content, "html.parser")
    for lien in soup.find_all('a', class_='nounder'):
        url = lien.get('href')
        if url not in liens_spam:
            liste_url.append(url)
    #penser à les saves

    return liste_url

def ouverture_liens(liste_url : List[str]) -> List[Page]:
    """Ouvre les différents liens des discussions du forums"""
    ##il faudra gérer quand il y'a des images dans les messages et des br
    ##dans certains cas la meilleure réponse peut se trouver sur un autre index de la page
    ## j'ai remarqué que lorsqu'une réponse était la meilleure au dessus de cette derniere se trouve un petit resumé du topic
    liste = []
    for lien in (liste_url):
        recuperation_sujet_dicussion = requests.get(lien)
        soup = BeautifulSoup(recuperation_sujet_dicussion.content, "html.parser")
        premier_message_bloc = soup.find("div", class_="first_message_bloc")
        meilleure_reponse = soup.find("div", class_="post_resume_topic disnone")
        if meilleure_reponse: ##cas où la meilleure réponse se trouve sur la même page 
            resultat_recupperation_question_reponse = Page(id=lien, lien=None, id_question=lien, id_reponse=lien, domaine=None, question=premier_message_bloc, reponse=meilleure_reponse)
        # else:  #cas où la réponse se trouve sur une page différente du sujet
        #     meilleure_reponse = soup.find("div", class_="rectangle_gris ultra_padding")
        #     lien_rectangle = meilleure_reponse.find("a")
        #     if lien_rectangle:
        #         lien_rectangle_href = lien_rectangle.get("href")
        #         recuperation_lien_meilleure_reponse = requests.get(lien_rectangle_href)
        #         soup = BeautifulSoup(recuperation_lien_meilleure_reponse.content, "html.parser")
       

    return resultat_recupperation_question_reponse             
            
def main():
    resultats_extraction = extraction_liens_forum("https://www.forumconstruire.com/construire/forum-51.php")
    print(ouverture_liens(resultats_extraction))


if __name__ == "__main__":
    main()

