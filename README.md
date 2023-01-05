# ZipTools

## Projet
ZipTools est un projet Django utilisant principalement les librairies zipfile et smtplib(mail), réalisé par Louis MAUPAS et Grégoire LE ROUX.

Il permet de mettre n'importe quel fichier zip et de pouvoir voir les fichiers à l'intérieur puis d'envoyer un mail avec le fichier zip en pièce-jointe.

## Prérequis
Python et les librairies zipfile, smtplib & dotenv

Fichier .env (se trouve dans le même dossier que manage.py) avec 3 variables d'environnement: EMAIL, PASSWORD et SERVER (Dans le mail de rendu du TP, le fichier est déjà présent)

## Comment lancer le projet ?
Se placer dans le dossier ziptools au même niveau que le fichier manage.py et faire la commande : ```python manage.py runserver```

Ensuite ouvrir un navigateur et se rendre sur l'adresse suivante: http://127.0.0.1:8000/
