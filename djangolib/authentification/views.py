from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from authentification.models import Utilisateur
import random
import string
from django.contrib.auth.decorators import login_required
from authentification.models import Utilisateur


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



@login_required
def comptes(request):
    regexMDP = "^(?=.[a-z])(?=.[A-Z])(?=.[0-9])(?=.[!@#$%^&*()_+-]).{8,}$"
    message = ""
    if request.method =="POST":
        ancienMDP = request.POST["ancienMDP"]
        nouveauMDP1 = request.POST["nouveauMDP1"]
        nouveauMDP2 = request.POST["nouveauMDP2"]

        verification = authenticate(username = request.user.username,
                                    password = ancienMDP)
        if verification != None:
            if nouveauMDP1 == nouveauMDP2:
                utilisateur = Utilisateur.objects.get(username = request.user.username)
                utilisateur.set_password(request.POST.get("nouveauMDP1"))
                utilisateur.save()
                return redirect("accueil")
            else:
                message = "Les deux mots de passe ne sont pas identiques"
        else:
            message = "Mot de passe incorrect"
    return render(request,
                  "comptes.html",
                  {"regexMDP": regexMDP, "message": message})