from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import re
from authentification.models import Utilisateur
import random
import string
from django.contrib.auth.decorators import login_required
from authentification.models import Utilisateur
from .forms import UtilisateurForm, ModificationMDPForm


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
    regexMDP = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-]).{8,}$"
    message = ""

    # Passer value='' au champ 'ancienMDP' pour éviter la pré-remplissage
    modification_mdp_form = ModificationMDPForm()
    utilisateur_form = UtilisateurForm(instance=request.user)

    if request.method == "POST":
        if "modification_mdp" in request.POST:
            modification_mdp_form = ModificationMDPForm(request.POST)
            if modification_mdp_form.is_valid():
                ancienMDP = modification_mdp_form.cleaned_data["ancienMDP"]
                nouveauMDP1 = modification_mdp_form.cleaned_data["nouveauMDP1"]
                nouveauMDP2 = modification_mdp_form.cleaned_data["nouveauMDP2"]

                verification = authenticate(username=request.user.username, password=ancienMDP)

                if verification is not None:
                    if nouveauMDP1 == nouveauMDP2 and re.match(regexMDP, nouveauMDP1):
                        utilisateur = Utilisateur.objects.get(username=request.user.username)
                        utilisateur.set_password(nouveauMDP1)
                        utilisateur.save()
                        return redirect("accueil")
                    elif nouveauMDP1 != nouveauMDP2:
                        message = "Les deux mots de passe ne sont pas identiques"
                    else:
                        message = "Les deux mots de passe ne respectent pas la contrainte."
                else:
                    message = "Mot de passe incorrect"

        elif "enregistrer" in request.POST:
            utilisateur_form = UtilisateurForm(request.POST, instance=request.user)
            if utilisateur_form.is_valid():
                utilisateur_form.save()

    return render(request, "comptes.html", {
        "regexMDP": regexMDP,
        "message": message,
        "modification_mdp_form": modification_mdp_form,
        "utilisateur_form": utilisateur_form,
    })

"""
def alimentationPatients():
    listePatients = pd.read_csv("/Users/narcy/Desktop/revision Django/doctolibbydjango/authentification/datas/listePatients.csv")
    for index, valeurs in listePatients.iterrows():
        #champDBB = Utilisateur._meta.get_fields()
        
        Utilisateur.objects.create_user(username = valeurs.username,
                                        password = valeurs.motDePasse,
                                        role="patient")
def alimentationMedecin():
    listeMedecins = pd.read_csv("/Users/narcy/Desktop/revision Django/doctolibbydjango/authentification/datas/listeMedecins.csv")
    for index, valeurs in listeMedecins.iterrows():
        Utilisateur.objects.create_user(username = valeurs.username,
                                        password = valeurs.motDePasse,
                                        role="medecin")
        
if len(Utilisateur.objects.filter(role="patient")) == 0:
    alimentationPatients()
if len(Utilisateur.objects.filter(role="medecin")) == 0:
    alimentationMedecin() 
"""