Semaine 1 : Choix du sujet et de la structuration des données

Objectif : J'aimerai réaliser une tache de Question Answering puisqu’il me semble que c’est une tâche essentielle que je pourrais rencontrer plus tard dans ma carrière en NLP.
En regardant les différents corpus sur HuggingFace fournis pour cette tâche on remarque que très peu des dataset sont réalisé sur des corpus en français.

Ma démarche pour choisir le dataset a été un peu laborieuse. Au début j’ai voulu prendre ce dataset:

1ere tentative : DILA-OPENDATA-FR-2023 :
https://huggingface.co/datasets/Nicolas-BZRD/DILA_OPENDATA_FR_2023/viewer/default/acco?p=2541   
Sauf que j’ai eu du mal à comprendre comment était structuré les questions et les réponses. Je crois qu’il y’a avait un document pour la question et un autre document pour les réponses.

2eme tentative : Je suis parti sur ce dataset ensuite fourni par le même utilisateur :  https://huggingface.co/datasets/Nicolas-BZRD/uld_loss_Mistral-7B-Instruct-v0.2-squad?row=25
Cela m’a permis d’identifier certaines patterns dans la structuration des datasets pour le Question Answering.
On retrouve souvent une colonne question, une autre réponse (logique) mais aussi une colonne contexte dans laquelle il faut préciser un peu pourquoi est posé cette question. Mais j’ai surtout l’impression que la réponse ce fait en fonction des éléments donnés dans le contexte.
De plus je n’étais pas trop satisfait car le corpus était en anglais et l’auteur a très peu détaillé son travail.

3eme tentative : Du coup j’ai continué à chercher et je suis tombé sur ce dataset qui prennait en compte du français : 
https://huggingface.co/datasets/almanach/hc3_french_ood
Ce dataset a été produit par une équipe ALMAnaCH du la boratoire de l’INRIA ?
Il a servi à plusieurs tâches : une tâche de classification du texte (en effet on observe dans la dernière colonne une colonne « etiquette » qui classifie si ça été écrit par un humain ou non. Une tâche de Questn Answering (logique c’est celle qui nous intéresse) on retrouve une colonne « question » et une colonne « réponse » et une tâche de «  Sentence Similarity ». En revanche, il n’y a pas de sous-tâche associée à ce dataset et aucun modèle ne semble l’utiliser à ce jour. Cela peut s’expliquer de par sa récente publication moins d’un an (en Juin 2023).

L’objectif de ce travail était de détecter si ChatGPT est facile à détecter en fonction des réponses.

Dans la structuration des données, je remarque qu’il n’y de colonne contexte dans laquelle il était nécéssaire de préciser le contexte de la question. La réponse semble être faite directement à partir de la page internet. 
Il y’a des colonnes id, page_id, answer_id, bucket et domain qui sont des identifiants qui permettent d’identifier de façon précise chaque question et réponse.

Ensemble de données en 2 parties :
    • First, an extension of the Human ChatGPT Comparison Corpus (HC3) dataset with French data automatically translated from the English source. 
    • Second, out-of-domain and adversarial French data set have been gathereed (Human adversarial, BingGPT, Native French ChatGPT responses). 



C’est surtout la 2eme parties qui va m’interesser pour le QA en français. 
« Out of modele » de ce que j’ai compris qui va m’interesser puisqu’on avec des sous ensembles de données tel que faq_fr_random et faq_fr_gouv. 
faq_fr_gouv la majorité des données proviennent de site .gouv (test: 235 exemples, 22336 mots)
faq_fr_random est un ensemble de données récupérés sur des sites random en français contenu dans le dataset MQA (Microsoft Question Answering), qui semble être une ressource contenant des questions et réponses sur divers sujets.



Pour la constitution de mon corpus je n’utiliserai pas les colonnes de classification et me contrerais que sur la tache de QA.




Pistes de réflexions pour la prochaine séances  
--------------------------------------------------------------
La tache explicitée la tache la sous tache s'il y'en a

Je me pose cependant encore quelques questions quant à la structuration du corpus : Tout d’abord où vais-je pouvoir me proccurer ce genre de corpus « open source » qui permet de faire du question answering (sur un forum ?, mais dans ce cas là il faudra anonymiser les données)
Quelles prédictions ? la taille des question et des réponses ?

questions  que je me pose comment je vais faire pour trouver les ressources (open sources) de
