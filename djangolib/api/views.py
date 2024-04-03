from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from transformers import pipeline

@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def qanda(request):
    message = ""
    question = ""
    if request.method == 'POST':
        print("THIS IS POST")
        question = request.POST.get("question", "")
        if not question:
            print("NO QUESTION MAAM")
            #erreur si pas de smiles ou pas de mask
            return render(request, "qanda.html", {"message": "Vous pouvez poser ici une question sur le fonctionnement de l'application."})

        # Récupérer les données de la requête POST (question et contexte)
        question = request.POST.get("question", "")
        print("QUESTION", question)
        context = """
                MedApp
        Résumé du contexte et de la demande
        Ce projet vise à créer une plateforme de gestion médicale. Un administrateur attribue des comptes aux médecins, peut consulter l'ensemble des patients inscrits ainsi que l'historique de leurs formulaires dans un tableau avec filtres dynamiques, attribuer des rôles et associer les patients à des médecins. Les médecins peuvent créer des comptes patients, mais pas les associer à un médecin. Ils peuvent voir l'historique des formulaires remplis par les patients qui leur sont associés dans un tableau avec filtres dynamiques, et modifier la périodicité à laquelle les patient doivent les remplir. Les patients remplissent des formulaires avec des informations médicales. Chaque utilisateur peut modifier son mot de passe et ses informations personnelles. Une suggestion de mot de passe respectant la contrainte est proposée au moment de l'inscription et au moment de la modification du mot de passe.
        
        Compétences visées
        Ce projet met en œuvre les compétences suivantes :
        
        Gestion des comptes utilisateur avec authentification
        Attribution des patients aux médecins
        Création, lecture, mise à jour et suppression (CRUD) des informations des patients
        Utilisation d'une base de données pour stocker les informations médicales
        Implémentation d'un système de recommandation de mot de passe
        Utilisation de Django pour le développement web
        Données (Schéma de la BDD)
        Le schéma de la base de données utilise les informations des formulaires fournies par les patients. Capture dcran 1 Schéma de la base de données authentification_utilisateur.username = colstress.user_id = colsante.user_id authentification_medecinpatient.idMedecin_id et authentification_medecinpatient.idPatient_id = authentification_utilisateur.id
        
        Mini Tutoriel pour Installer le Projet sur un Poste et le Lancer
        Prérequis
        Python installé sur votre machine
        Virtualenv pour isoler l'environnement de développement
        Étapes d'Installation
        Clonez le repository
        Créez un environnement virtuel : python -m venv venv
        Activez l'environnement virtuel :
        Sur Windows : venv\Scripts\activate
        Sur MacOS/Linux : source venv/bin/activate
        Installez les dépendances : pip install -r requirements.txt
        Créez les migrations pour la partie authentification : python manage.py makemigrations authentification
        Appliquez les migrations pour la partie authentification : python manage.py migrate authentification
        Créez les autres migrations : python manage.py makemigrations
        Appliquez les autres migrations : python manage.py migrate
        Créez un superutilisateur : python manage.py createsuperuser
        Lancez le serveur de développement : python manage.py runserver
        Le projet sera disponible à l'adresse http://localhost:8000. Connectez-vous avec le superutilisateur pour commencer.
        
        Screenshots du Résultat Final
        Capture dcran 2 Page d'association médecin/patient, admin VS médecin
        
        Capture dcran 3 Page de création d'un nouveau compte, admin VS médecin
        
        Capture dcran 4 Page du questionnaire de santé générale, patient VS médecin
        
        Capture dcran 4 Page du questionnaire de stress, patient VS médecin
        
        Capture dcran 4 Page de l'historique patient
        
        Capture dcran 4 Page de modification du compte
        
        Versions Futures
        La version actuelle met en place les fonctionnalités de base. Les versions futures pourraient inclure :
        
        Ajout EDA et IA avec alertes
        Ajout CSS
        Intégration de tests unitaires
        Mise en place de l'envoi d'email avec indentifiants
        Modification du mdp obligatoire à la première connexion
        Gestion des fuseaux horaires, devises, mesures
        """

        # Charger le modèle de question-réponse
        qa_model = pipeline('question-answering', model='Nadav/bert-base-french-europeana-cased-squad-fr')

        # Effectuer la prédiction de question-réponse
        answer = qa_model(question=question, context=context)
        result = answer['answer']


        # Renvoyer une réponse JSON avec les résultats
        return render(request, "qanda.html", {"result": result})
    else:
        #si la méthode n'est pas POST
        return render(request, "qanda.html", {"message": "Vous pouvez poser ici une question sur le fonctionnement de l'application."})

