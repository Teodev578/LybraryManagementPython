# LybraryManagementPython
```
# Projet de Gestion de Livres

Ce projet est une application de gestion de livres développée en Python utilisant la bibliothèque `customtkinter` pour l'interface utilisateur graphique et MySQL pour la base de données. L'application permet de gérer une collection de livres en ajoutant, modifiant et supprimant des entrées de la base de données. Les fonctionnalités principales incluent l'affichage des livres dans une liste, la recherche de livres et la gestion des images de couverture.

## Prérequis

- Python 3.x
- Bibliothèques Python : `customtkinter`, `mysql-connector-python`, `PIL`
- Serveur MySQL avec une base de données nommée `Lybrary` et une table `Livre`

## Installation des bibliothèques Python

Vous pouvez installer les bibliothèques nécessaires en utilisant `pip` :

```

pip install customtkinter mysql-connector-python Pillow

```

## Configuration de la base de données

Créez une base de données MySQL nommée `Lybrary` et une table `Livre` avec les colonnes suivantes :

```sql
CREATE TABLE Livre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    isbn VARCHAR(20),
    publisher VARCHAR(255),
    years INT,
    copies INT,
    descriptions TEXT,
    category VARCHAR(255),
    cover VARCHAR(255)
);

```

## Exécution de l'application

Pour exécuter l'application, assurez-vous que votre serveur MySQL est en cours d'exécution et que les informations de connexion dans le fichier main.py sont correctes. Ensuite, lancez le fichier principal :

```
python <nom_du_fichier_principal>.py

```

## Auteur

Ce projet a été développé par Fabien.
