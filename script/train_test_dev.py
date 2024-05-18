"""Ce script va découper mon corpus en plusieurs fichiers tsv train, test, dev """

import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple


def split_train_test_dev()-> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: ## pour pouvoir signer ma fonction correctement j'ai mis les returns dans un tuple

    """
    Divise le corpus en sous-ensembles d'entraînement, de test et de validation (dev).

    Cette fonction lit le corpus à partir d'un fichier TSV, puis utilise la fonction
    train_test_split de la librairie sckipit-learn pour diviser les données en 70% pour l'entraînement, 
    15% pour le test et 15% pour la validation (dev).

    Parametres:
    None
  
    Returns : 
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Un tuple contenant les ensembles
        d'entraînement, de test et de dev.
    """

    data = pd.read_csv('../data/dataset/dataset_complet.tsv', sep='\t', skiprows=[0]) ## utilisation de pandas et de sa méthode read_csv afin d'avoir une dataframe de mon fichier csv
    train_data, temp_data = train_test_split(data, test_size=0.3, shuffle=True, random_state=0) ## 70% train, 30% test
    print(type(train_data))
    dev_data, test_data = train_test_split(temp_data, test_size=0.5, shuffle=True, random_state=0) ## on divise les données de test par 2 donc 15% de données pour le dev
    return train_data, test_data, dev_data

def ecriture_resultats(train_data, test_data, dev_data) -> None:
    """
    Écrit les données d'entraînement, de test et de dev dans des fichiers CSV.

    Cette fonction prend en entrée les données d'entraînement, de test et de dev
    sous forme de DataFrames pandas, puis les écrit dans des fichiers CSV nommés
    'train_data.csv', 'test_data.csv' et 'dev_data.csv' dans le répertoire '../data/train_test_dev/'.

    Parametres:
        train_data (pd.DataFrame): Les données d'entraînement.
        test_data (pd.DataFrame): Les données de test.
        dev_data (pd.DataFrame): Les données de validation.
  

    Returns : 
        None
    """

    train_data.to_csv('../data/train_test_dev/train_data.csv', index=False) ## index false pour ne pas avoir l'id des lignes csv
    test_data.to_csv('../data/train_test_dev/test_data.csv', index=False)
    dev_data.to_csv('../data/train_test_dev/dev_data.csv', index=False)


def main():

    train_data, test_data, dev_data = split_train_test_dev()
    ecriture_resultats(train_data, test_data, dev_data)
    


if __name__ == "__main__":
    main() 