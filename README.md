# MedApp


## Résumé du contexte et de la demande

Ce projet vise à créer une plateforme de gestion médicale permettant de recueillir des données de santé auprès de patients volontaires via deux formulaires, et ce à deux fins:
- simplifier le suivi des patients inscrits
- obtenir des données générales qui seront anonymisées et agrégées afin d'obtenir une vue d'ensemble de la santé en France.  
Un administrateur attribue des comptes aux médecins, peut consulter l'ensemble des patients inscrits ainsi que l'historique de leurs réponses aux formulaires dans un tableau avec filtres dynamiques, attribuer des rôles (médecin, patient, administrateur) et associer les patients à des médecins traitants.  
Les médecins peuvent créer des comptes patients, mais pas les associer à un médecin. Ils peuvent voir l'historique des formulaires remplis par les patients qui leur sont associés dans un tableau avec filtres dynamiques, et modifier la périodicité à laquelle les patient doivent les remplir.
Les patients remplissent des formulaires avec des informations médicales:
- un formulaire de santé générale (taille, poids, sympptômes, médicaments, consommation, activité physique)
- un formulaire sur la fréquence d'apparition de symptômes de stress, à remplir avec une note de 0 à 10:
	- 0: Ce symptôme n’est pas apparu au cours des deux dernières semaines
	- 1: Ce symptôme est apparu une ou deux fois seulement au cours des deux dernières semaines
	- 5: Ce symptôme est apparu plusieurs fois au cours des deux dernières semaines
	- 10: Ce symptôme est apparu presque continuellement au cours des deux dernières semaines.  

Chaque utilisateur peut modifier son mot de passe et ses informations personnelles. Une suggestion de mot de passe respectant les contraintes de sécurité est proposée au moment de l'inscription et au moment de la modification du mot de passe. Les contraintes de sécurité sont les suivantes:
- La longueur minimale du mot de passe est de 8 caractères.
- Il doit contenir au moins une lettre minuscule (a-z).
- Il doit contenir au moins une lettre majuscule (A-Z).
- Il doit contenir au moins un chiffre (0-9).
- Il doit contenir au moins un caractère spécial parmi !@#$%^&*()_+-.  

De plus, une partie intelligence artificielle (question answering) permet aux patients comme aux médecins de poser des questions sur le fonctionnement de l’application et d’obtenir une réponse en temps réel et à tout moment, sans attendre l’intervention d’un administrateur, remplaçant ainsi la présence d'une FAQ.

## Compétences visées

Ce projet met en œuvre les compétences suivantes :
- Gestion des comptes utilisateur avec authentification
- Attribution des patients aux médecins
- Création, lecture, mise à jour et suppression (CRUD) des informations des patients
- Utilisation d'une base de données pour stocker les informations médicales
- Implémentation d'un système de recommandation de mot de passe
- Utilisation de Django pour le développement web
- Mise à disposition d'un modèle d'intelligence artificielle

## Données

![Capture d'écran 1](https://github.com/meowd18/medapp/blob/resolve/img/double_db.jpg)
*Schéma simplifié de la base de données*  
*authentification_utilisateur.username = colstress.user_id = colsante.user_id*  
*authentification_medecinpatient.idMedecin_id et authentification_medecinpatient.idPatient_id = authentification_utilisateur.id*

## Installation du Projet

### Prérequis
- Python installé sur votre machine
- Virtualenv pour isoler l'environnement de développement

### Étapes d'Installation
1. Clonez le repository
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
    - Sur Windows : `venv\Scripts\activate`
    - Sur MacOS/Linux : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`
5. Créez les migrations pour la partie authentification : `python manage.py makemigrations authentification`
6. Appliquez les migrations pour la partie authentification : `python manage.py migrate authentification`
7. Créez les autres migrations : `python manage.py makemigrations`
6. Appliquez les autres migrations : `python manage.py migrate`
8. Créez un superutilisateur : `python manage.py createsuperuser`
9. Lancez le serveur de développement : `python manage.py runserver`

Le projet sera disponible à l'adresse [http://localhost:8000](http://localhost:8000). Connectez-vous avec le superutilisateur pour commencer.

## Apperçus

![Capture d'écran 2](https://github.com/meowd18/medapp/blob/resolve/img/association.png)
*Page d'association médecin/patient, admin VS médecin*

![Capture d'écran 3](https://github.com/meowd18/medapp/blob/resolve/img/nouveau_compte.png)
*Page de création d'un nouveau compte, admin VS médecin*

![Capture d'écran 4](https://github.com/meowd18/medapp/blob/resolve/img/sante_generale.png)
*Page du questionnaire de santé générale, patient VS médecin*

![Capture d'écran 4](https://github.com/meowd18/medapp/blob/resolve/img/stress.png)
*Page du questionnaire de stress, patient VS médecin*

![Capture d'écran 4](https://github.com/meowd18/medapp/blob/resolve/img/historique.png)
*Page de l'historique patient*

![Capture d'écran 4](https://github.com/meowd18/medapp/blob/resolve/img/mon_compte.png)
*Page de modification du compte*

![Capture d'écran 5](https://github.com/meowd18/medapp/blob/resolve/img/q_and_a.png)
*Page de question-réponse via IA*

## Surveillance d'application

La surveillance de l'application est effectuée à l'aide de MLflow, où les incidents d'accès à la base de données sont consignés lors de l'envoi d'un formulaire par un patient.  
Pour accéder au tableau de bord MLflow, depuis le repertoire medapp exéctuez:  
`mlflow ui --backend-store-uri sqlite:///mlflow.db`  
et sélectionnez l'expérience nommée *database_access_monitoring*

## Versions Futures et de Production

La version actuelle met en place les fonctionnalités de base. Les versions futures pourraient inclure :
- Ajout EDA (graphiques par patient, par tranches d'âge etc.) et alertes en cas de franchissement de seuil
- Ajout CSS
- Mise en place de l'envoi d'email avec indentifiants
- Modification du mdp obligatoire à la première connexion
- Gestion des fuseaux horaires, devises, mesures

En développement, une seule base de données à été utilisées pour simplifier la gestion. Cependant, en production, les données d'authentification et les données médicales devront être stockées dans deux bases de données distinctes.
