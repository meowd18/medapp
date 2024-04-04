from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from transformers import pipeline
from .context import ctxt

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
        context = ctxt

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

