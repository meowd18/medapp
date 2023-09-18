from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

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
            #return render(request, message)
    else:
        return render(request,
                      "connexion.html", {"message": message})

def deco(request):
    logout(request)
    return redirect("connexion")

