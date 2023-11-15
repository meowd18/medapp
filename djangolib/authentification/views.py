from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import re
from authentification.models import Utilisateur
import random
import string
from django.contrib.auth.decorators import login_required
from authentification.models import Utilisateur
from .forms import UtilisateurForm, ModificationMDPForm, UtilisateurFullForm
from django.http import JsonResponse
from django.contrib import messages

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


def get_last_username(request, role):
    last_username = Utilisateur.objects.filter(role=role).order_by('-username').first()
    if last_username:
        return JsonResponse({'last_username': last_username.username})
    else:
        return JsonResponse({'last_username': ''})

@login_required
def nouveau_compte(request):
    if request.user.role == "responsable":
        roles = Utilisateur.objects.values_list('role', flat=True).distinct()
        roles.append("")
    elif request.user.role == "medecin":
        roles = ["patient"]
        roles.append("")

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        role = request.POST["role"]
        is_superuser = request.POST.get("is_superuser", "0")
        username = request.POST["username"]
        motDePasse = request.POST["motDePasse"]

        # Vérifier si l'utilisateur avec cet identifiant existe déjà
        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, 'Cet identifiant est déjà pris.')
        else:
            nouveauCompte = Utilisateur.objects.create_user(
                username=username,
                password=motDePasse,
                first_name=first_name,
                role=role,
                is_superuser=is_superuser,
                last_name=last_name,
                email=email
            )
            messages.success(request, 'Compte créé avec succès.')

    # Ajoutez les messages flash dans le contexte de rendu de la page
    success_messages = [str(message) for message in messages.get_messages(request)]

    return render(request, "nouveau_compte.html", {
        "roles": roles,
        "success_messages": success_messages,
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