# Doctolib-_-Maud


## Résumé du contexte et de la demande

Ce projet vise à créer une plateforme de gestion médicale. Un administrateur attribue des comptes aux médecins, peut consulter l'ensemble des patients inscrits ainsi que l'historique de leurs formulaires dans un tableau avec filtres dynamiques, attribuer des rôles et associer les patients à des médecins.
Les médecins peuvent créer des comptes patients, mais pas les associer à un médecin. Ils peuvent voir l'historique des formulaires remplis par les patients qui leur sont associés dans un tableau avec filtres dynamiques, et modifier la périodicité à laquelle les patient doivent les remplir.
Les patients remplissent des formulaires avec des informations médicales.
Chaque utilisateur peut modifier son mot de passe et ses informations personnelles. Une suggestion de mot de passe respectant la contrainte est proposée au moment de l'inscription et au moment de la modification du mot de passe.

## Compétences visées

Ce projet met en œuvre les compétences suivantes :
- Gestion des comptes utilisateur avec authentification
- Attribution des patients aux médecins
- Création, lecture, mise à jour et suppression (CRUD) des informations des patients
- Utilisation d'une base de données pour stocker les informations médicales
- Implémentation d'un système de recommandation de mot de passe
- Utilisation de Django pour le développement web

## Données (Schéma de la BDD)

Le schéma de la base de données utilise les informations des formulaires fournies par les patients.
![Capture d'écran 1](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/schema_bdd.png)
*Schéma de la base de données*
*authentification_utilisateur.username = colstress.user_id = colsante.user_id*
*authentification_medecinpatient.idMedecin_id et authentification_medecinpatient.idPatient_id = authentification_utilisateur.id*

## Mini Tutoriel pour Installer le Projet sur un Poste et le Lancer

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
7. Créez les migrations pour la partie application : `python manage.py makemigrations application`
6. Appliquez les migrations pour la partie application : `python manage.py migrate application`
8. Créez un superutilisateur : `python manage.py createsuperuser`
9. Lancez le serveur de développement : `python manage.py runserver`

Le projet sera disponible à l'adresse [http://localhost:8000](http://localhost:8000). Connectez-vous avec le superutilisateur pour commencer.

## Screenshots du Résultat Final

![Capture d'écran 2](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/association.png)
*Page d'association médecin/patient, admin VS médecin*

![Capture d'écran 3](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/nouveau_compte.png)
*Page de création d'un nouveau compte, admin VS médecin*

![Capture d'écran 4](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/sante_generale.png)
*Page du questionnaire de santé générale, patient VS médecin*

![Capture d'écran 4](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/stress.png)
*Page du questionnaire de stress, patient VS médecin*

![Capture d'écran 4](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/historique.png)
*Page de l'historique patient*

![Capture d'écran 4](https://github.com/data-IA-2022/Doctolib-_-Maud/blob/main/img/mon_compte.png)
*Page de modification du compte*


## Versions Futures

La version actuelle met en place les fonctionnalités de base. Les versions futures pourraient inclure :
- Ajout EDA et IA avec alertes
- Ajout CSS
- Intégration de tests unitaires
- Mise en place de l'envoi d'email avec indentifiants
- Modification du mdp obligatoire à la première connexion
- Gestion des fuseaux horaires, devises, mesures
