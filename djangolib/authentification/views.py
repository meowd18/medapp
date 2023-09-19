from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from authentification.models import Utilisateur
import random
import string

# Create your views here.
def connexion(request):
    message = ""
    #si qqun a cliqué sur VALIDER id + mdp
    if request.method == "POST":
        username = request.POST["username"]
        mdp = request.POST["mdp"]
        verification = authenticate(username = username,
                                    password = mdp)
        if verification != None:
            login(request, verification)
            return redirect("accueil")
        else:
            message = "username et/ou mdp inconnu"

    return render(request,
                      "connexion.html", {"message": message})

def deco(request):
    logout(request)
    return redirect("connexion")

def inscription(request):
    ideeMDP = "".join([random.choice(string.printable) for _ in range(12)]).replace(" ", "")
    if request.method == "POST":
        username = request.POST["username"]
        motDePasse = request.POST["motDePasse"]
        nouveauCompte = Utilisateur.objects.create_user(username = username,
                                                        password = motDePasse)

        return redirect("connexion")

    return render(request,
                  "inscription.html", {"ideeMDP" : ideeMDP.replace(" ", "")})