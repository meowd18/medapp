from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ColStressForm, ColSanteForm
from authentification.models import Utilisateur, medecinPatient
from datetime import date

#from .models import col_stress

# Create your views here.
@login_required
def accueil(request):
    prenom = request.user.username
    return render(request,
                  "accueil.html",
                  context={"prenom": prenom})

@login_required
def data_stress(request):
    prenom = request.user.username
    initial_data = {'prénom': prenom}
    initial_data['date'] = date.today().strftime('%d/%m/%Y')

    if request.method == 'POST':
        form = ColStressForm(request.POST, initial=initial_data)
        if form.is_valid():
            # Calculer le total à partir des valeurs des champs du formulaire
            total = 0
            for field_name in form.fields:
                if field_name != 'user_id' and field_name != 'date':
                    total += form.cleaned_data[field_name]

            # Enregistrez le total dans le formulaire
            form.instance.total_de_limpact_du_stress_dans_votre_vie_actuelle = total
            form.save()

            return redirect('accueil')  # Redirigez vers une page de confirmation

    else:
        form = ColStressForm(initial=initial_data)

    return render(request, 'data_stress.html', {'form': form})


@login_required
def data_sante(request):
    prenom = request.user.username
    initial_data = {'prénom': prenom}
    initial_data['date'] = date.today().strftime('%d/%m/%Y')
#col_stress = col_stress.objects.all()
    if request.method == 'POST':
        form = ColSanteForm(request.POST, initial=initial_data)
        if form.is_valid():
            form.save()
            return redirect('accueil')  # Redirigez vers une page de confirmation
    else:
        form = ColSanteForm(initial=initial_data)

    return render(request, 'data_sante.html', {'form': form})

#interdire accès à une page en fonction du rôle
'''if request.user.role != "medecin":
    return redirect ("accueil") #ou autre page disant que fais-tu là
else:
    return render (request, "page en question")'''


@login_required
def association(request):
    # 1- Récupérer la liste des id des médecins et des patients
    # 2- Ensuite on ne garde que les patients qui ne sont pas dans la table medecinPatient
    # 3- On créé ensuite un template qui contiendra une liste déroulante
    # 4- Dans cette liste déroulante on va afficher d'un côté les médecins
    # et de l'autre les patients filtrés (voir étapge 2)
    # https://developer.mozilla.org/fr/docs/Web/HTML/Element/select
    medecinsID = [medecin.id for medecin in Utilisateur.objects.filter(role="medecin")]
    patientsID = [patient.id for patient in Utilisateur.objects.filter(role="patient")]
    listePatientsAssocies = [ligne.idPatient for ligne in medecinPatient.objects.all()]
    listePatientsNonAssocies = [id for id in patientsID if id not in listePatientsAssocies]
    tableAssociation = medecinPatient.objects.all()
    # Syntaxte équivalente
    #for id in patientsID :
    #    if id not in listePatientsAssocies:
    #        patientsNonAssocies.append(id)

    if request.method == "POST":
        medecin = request.POST["medecin"]
        patient = request.POST["patient"]
        medecinPatient(idMedecin = Utilisateur.objects.filter(id=medecin)[0],
                       idPatient = Utilisateur.objects.filter(id=patient)[0]).save()
        #medecinPatient.save()
    return render(request, "association.html",
                  {"listePatientsNonAssocies" : listePatientsNonAssocies,
                   "medecinsID" : medecinsID,
                   "tableAssociation" : tableAssociation})

#print(list(utilisateur.username for utilisateur in Utilisateur.objects.filter(role="medecin")))

'''
list1 = [utilisateur.username for utilisateur in Utilisateur.objects.filter(role="medecin")]
for utilisateur in Utilisateur.objects.filter(role="patient"):
    if not medecinPatient.objects.filter(idPatient=utilisateur).exists():
        list1.append(utilisateur.username)
print(list1)
'''
