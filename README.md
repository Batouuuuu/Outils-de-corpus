dataset:
  name: "jeu de données de questions et réponses en français sur un forum de bricolage"
  pretty_name: "Questions et réponses forum bricolage"
  description: |
    Ce jeu de données contient les questions et les réponses des utilisateurs récupérées sur un forum de bricolage.
    Il est conçu pour des tâches de traitement du langage naturel telles que le question answering et la classification.
langues: 
  - fr
tags:
  - NLP
  - French
inspirations:
  - name: "hc3_french_ood"
    url: "https://huggingface.co/datasets/almanach/hc3_french_ood"
    description: "Un corpus de textes pour une tâche de question answering issu de plusieurs sites du gouvernement."
license: "Creative Commons Attribution-ShareAlike 4.0 International"
task_categories:
  - Question Answering
  - Classification
collection_process:
  - description: "Les données ont été collectées à partir de plusieurs pages d'un même forum."
  - methodology: "Scraping des pages du forum car aucune mention légale n'apparaissait sur le site. J'ai donc déduit que le scraping en anonymisant les utilisateurs était autorisé."
additional_information:
  - url: "https://www.forumconstruire.com/construire/forum-51.php"
  - author: "Gillet Baptiste"
