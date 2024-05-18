"""Script princial. Il récuppère les questions et les réponses du forum : 
https://www.forumconstruire.com/construire/topic-474537-meilleur-protection-anti-rouille.php#6365329  les stock dans des dataclass
pour enfin ecrire les différents objets des dataclass dans un fichier tsv"""

import csv
import requests
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from datastructures import Page, Dataset



def extraction_liens_forum(page_accueil : str | Path)-> List[str]:
    """
    Extrait les liens de discussions depuis une page du forum.

    Cette fonction prend l'URL ou le chemin local de la page principale d'un forum, 
    extrait tous les liens menant à des discussions en excluant les liens de spam, 
    et les renvoie sous forme de liste.

    Parametres:
    page_accueil (str | Path): L'URL ou le chemin du fichier de la page principale du forum.

    Return:
    List[str]: Une liste de liens uniques menant aux discussions du forum.
    """
    
    set_url = set() ## je ne sais pas pourquoi j'avais des doublons j'ai donc tout stocké dans un set
    URL = requests.get(page_accueil) 
    ##retirer les pubs
    liens_spam = ["https://www.forumconstruire.com/construire/devis-0-66-devis_renovation.php","https://achat.forumconstruire.com/vente-privee/"]
    soup = BeautifulSoup(URL.content, "html.parser")
    for lien in soup.find_all('a', class_='nounder'):
        url = lien.get('href')
        if url not in liens_spam:
            set_url.add(url)
    liste_url = list(set_url) ## je convertis en liste car sinon j'ai des problèmes pour manipuler les indices dans l'itération de ma dataclass
    return liste_url


def ouverture_liens(liste_url : List[str]) -> List[BeautifulSoup]:
    """
    Ouvre les différents liens des discussions du forum, récupère tout leur contenu et balisage HTML, 
    vérifie s'ils contiennent une "meilleure réponse" et stocke le tout dans une liste.

    Cette fonction prend une liste d'URLs de discussions du forum, effectue une requête HTTP pour chaque URL, 
    analyse le contenu HTML de chaque page, vérifie la présence d'une meilleure réponse et 
    ajoute le contenu HTML analysé à une liste si cette condition est remplie.

    Parametres:
    liste_url (List[str]): Une liste d'URLs menant aux discussions du forum.

    Returns:
    List[BeautifulSoup]: Une liste d'objets BeautifulSoup représentant le contenu HTML des pages 
                         contenant la meilleure réponse.
    """

    liste_soup = []
    for lien in liste_url:
        recuperation_sujet_dicussion = requests.get(lien)
        soup = BeautifulSoup(recuperation_sujet_dicussion.content, "html.parser", from_encoding="utf-8")
        ## maintenant on cherche si dans le contenu de ces pages ont retrouve l'intitulé "meilleure réponse"
        div_tag = soup.find('div', class_='rectangle_gris ultra_padding')
        if div_tag:
            a_tag = div_tag.find('a')
            if a_tag:
                liste_soup.append(soup) ## on le trouve donc on ajoute le contenu de cette page dans une liste
    return liste_soup
        

def recuperation_question(soup_liste : List[BeautifulSoup]) -> List[str]:
    """
    Récupère et prétraite les questions à partir d'une liste de contenus HTML.

    Cette fonction parcourt une liste d'objets BeautifulSoup ( le contenu HTML des pages 
    de discussions du forum), extrait le texte des blocs de première question et retourne une liste 
    de ces questions sous forme de chaînes de caractères.

    Parametres:
    soup_liste (List[BeautifulSoup]): Une liste d'objets BeautifulSoup représentant les contenus HTML 
                                      des pages de discussions du forum.

    Returns:
    List[str]: Une liste de chaînes de caractères, chaque chaîne représentant une question extraite 
               d'une page de discussion.
    """
    
    liste_question = []
    for numero,soup in enumerate(soup_liste):
        premier_message_bloc = soup.find("div", class_="first_message_bloc")
        if premier_message_bloc: ##des fois il peut ne pas y avoir de question si c'est le cas alors on ne prend pas en compte cette question
            question = premier_message_bloc.get_text(separator=" ", strip=True)
            # print(f"question numéro {numero }: {question}")
            liste_question.append(question)
    return liste_question

def recuperation_sujet_question(soup_list: List[BeautifulSoup]) -> List[str]:
    ## Cette fonction est quasi identique à celle de la récupération des questions j'aurais pu tout unifier dans une fonction
    """
    Récupère les sujets des questions.

    Cette fonction parcourt une liste d'objets BeautifulSoup et extrait le texte 
    des sujets des questions et retourne une liste de ces sujets sous forme de chaînes 
    de caractères, en évitant les doublons.

    Parametres:
    soup_list (List[BeautifulSoup]): Une liste d'objets BeautifulSoup représentant les contenus HTML 
                                     des pages de discussions du forum.

    Returns:
    List[str]: Une liste de chaînes de caractères, chaque chaîne représentant un sujet de question 
               extrait d'une page de discussion, sans doublons.
    """
    
    sujets = set()  ## j'utilise encore un set pour éviter les doublons
    for soup in soup_list:
        div_tag = soup.find('div', class_='ultra_padding_iphone')
        if div_tag:
            a_tag = div_tag.find('a')
            if a_tag:
                sujet = a_tag.get_text(strip=True)
                sujets.add(sujet)  
        conversion_liste = list(sujets)  ## je convertis notre set en liste puisque cela nous permettra de zip toutes les listes pour pouvoir les parcourir dans le main
    return conversion_liste



def sauvegardes_questions(chemin_fichier : str | Path, liste_question : List[str]) -> None:
    ## cette fonction est une vérification, elle n'est pas utilisée dans le main, cela permettait de voir si les questions étaient bien extraites et sans doublons
    """
    Sauvegarde les questions dans un fichier texte.

    Cette fonction écrit chaque question de la liste fournie dans un fichier texte spécifié. 
    Chaque question est précédée de son numéro de ligne.

    Parametres:
    chemin_fichier (str | Path): Le chemin du fichier où les questions seront sauvegardées.
    liste_question (List[str]): Une liste de chaînes de caractères, chaque chaîne représentant une question.

    Returns:
    None
    """

    with open(chemin_fichier, "w", encoding='UTF8') as resultat:
        for numero,question in enumerate(liste_question):
            resultat.write(f"Question {numero}: {question}\n") 


def url_meilleurs_reponse(liste_url : List[str]) -> List[str]:
    """
    Récupère l'URL de la meilleure réponse à partir d'une liste d'URLs et les ajoute dans une liste.

    Cette fonction parcourt une liste d'URLs de discussions du forum, effectue une requête HTTP 
    pour chaque URL, analyse le contenu HTML de chaque page, extrait l'URL de la meilleure réponse 
    si elle existe, et les ajoute à une liste. Cette liste est ensuite retournée.

    Parametres:
    liste_url (List[str]): Une liste d'URLs menant aux discussions du forum.

    Returns:
    List[str]: Une liste d'URLs menant aux meilleures réponses des discussions du forum.
    """
    
    url_meilleurs_reponse = []
    # print(len(liste_url))
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
    """
    Parcourt les URLs des réponses et récupère la réponse avec le plus de likes.

    Cette fonction parcourt une liste d'URLs, analyse le contenu HTML de chaque page pour trouver 
    les likes de chaque réponse, puis récupère la réponse avec le plus de likes. 
    Elle renvoie une liste contenant la meilleure réponse de chaque URL.

    Parametres:
    liste_URL_reponse (List[str]): Une liste d'URLs menant aux réponses du forum.

    Returns:
    List[str]: Une liste contenant la meilleure réponse de chaque URL.
    """
    
    comments_likes = []
    liste_meilleure_reponse = []
    # print(len(liste_URL_reponse))
    for lien in liste_URL_reponse:
        # print(lien)
        response = requests.get(lien)
        soup = BeautifulSoup(response.content, 'html.parser')
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


def ecriture_resultat_tsv(dataset_fichier : str | Path, data : Dataset) -> None:
    """
    Écrit les résultats dans un fichier TSV.

    Cette fonction prend en entrée un chemin de fichier et un objet Dataset. 
    Elle écrit ces données dans un fichier TSV avec les colonnes suivantes : ID, URL, 
    Question_ID, Reponse_ID, Sujet, Question, Reponse, Etiquette.

    Parametres:
    dataset_fichier (str |Path): Le chemin du fichier où les résultats seront écrits.
    data (Dataset): Un objet Dataset contenant les données à écrire dans le fichier.

    Returns:
    None
    """

    with open(dataset_fichier, "w", newline='', encoding='UTF-8') as resultats_tsv:
        ecriture = csv.writer(resultats_tsv, delimiter="\t")
        ecriture.writerow(["ID", "URL","Question_ID", "Reponse_ID", "Sujet", "Question", "Reponse", "Etiquette"])
        
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

    liste = []
    resultats_extraction = extraction_liens_forum("https://www.forumconstruire.com/construire/forum-51.php")
    soup_liste = ouverture_liens(resultats_extraction)
    sujets = recuperation_sujet_question(soup_liste)
    questions = recuperation_question(soup_liste)
    reponses_URL = url_meilleurs_reponse(resultats_extraction)
    reponses = recuperation_meilleure_reponse(reponses_URL)
    
    ##parcours de tous nos résultats zippés et ajout dans notre dataclass
    for i, (url, question, reponse, sujet) in enumerate(zip(resultats_extraction, questions, reponses, sujets), start=1):
        extraction = Page(
            id=i,
            lien=url,
            id_question=i,
            id_reponse=i,
            sujet=sujet,
            question=question,
            reponse=reponse,
            etiquette="HUMAIN" ## car i; s'agit de réponses humaines
        )
        liste.append(extraction)
    
    dataset = Dataset(data=liste) ## création d'un objet Dataset contenant nos données extraites 
    
    # for page in dataset.data:
    #     print(page)

    with open('../data/corpus/', "w") as fichier:
        fichier = dataset.data
        for page in fichier:
            fichier.write(page)

    ecriture_resultat_tsv('../data/dataset/test.tsv', dataset)



if __name__ == "__main__":
    main()

