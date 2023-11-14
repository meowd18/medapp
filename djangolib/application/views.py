from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ColStressForm, ColSanteForm
from .models import ColSante, ColStress
from authentification.models import Utilisateur, medecinPatient
from datetime import date
import numpy as np

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
    if request.user.role != "patient":
        return redirect ("accueil")
    else:
        prenom = request.user.username
        initial_data = {'prénom': prenom}
        initial_data['date'] = date.today().strftime('%d/%m/%Y')

        if request.method == 'POST':
            form = ColStressForm(request.POST, initial=initial_data)
            if form.is_valid():
                # Calculer le total à partir des valeurs des champs du formulaire
                total = 0
                for field_name, field_value in form.cleaned_data.items():
                    if field_name != 'user_id' and field_name != 'date':
                        if field_value is not None:
                            total += field_value

                # Enregistrez le total dans le formulaire
                form.instance.total_de_limpact_du_stress_dans_votre_vie_actuelle = total
                form.save()

                return redirect('accueil')  # Redirigez vers une page de confirmation

        else:
            form = ColStressForm(initial=initial_data)

        return render(request, 'data_stress.html', {'form': form})




@login_required
def data_sante(request):
    if request.user.role != "patient":
        return redirect ("accueil")
    else:
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
def stress_datatable(request):
    pat = []
    for p in medecinPatient.objects.filter(idMedecin = request.user.id).values():
        username_pat = Utilisateur.objects.filter(id = p["idPatient_id"])[0].username
        pat.append([el.values() for el in ColStress.objects.filter(user_id = username_pat).values()])
    try:
        pat = list(np.concatenate(pat).flat)
    except:
        pat = pat

    # Je récupère les champs de la table formulaire santé
    champsFormulaireStress = [field.name for field in ColStress._meta.get_fields()]
    # Je récupère les ids des lignes de la table formulaire santé
    idDesFormulairesStr = [valeur.id for valeur in ColStress.objects.all()]
    # Je crée une liste qui contiendra les valeurs des lignes
    # Il y a autant d'élément que de ligne, donc que d'ids récupéré
    # FormulaireSante.objects.filter(id=id).values()[0].values()
    # Dans le code ci-dessus je récupère la ligne ayant un certain id
    # Ensuite je récupère les valeurs de la ligne .values
    # Le 1er élément qui est le dictionnaire des colonnes/valeurs
    # et enfin uniquement les valeurs
    dataFormulaireStress = [ColStress.objects.filter(id=id).values()[0].values() for id in idDesFormulairesStr]
    dataFormulaireStress_med = pat
    return render(request, "stress_datatable.html",
                  {"dataFormulaireStress" : dataFormulaireStress,
                   "dataFormulaireStress_med" : dataFormulaireStress_med,
                   "champsFormulaireStress" : champsFormulaireStress})
@login_required
def sante_datatable(request):
    pat = []
    for p in medecinPatient.objects.filter(idMedecin = request.user.id).values():
        username_pat = Utilisateur.objects.filter(id = p["idPatient_id"])[0].username
        pat.append([el.values() for el in ColSante.objects.filter(user_id = username_pat).values()])
    try:
        pat = list(np.concatenate(pat).flat)
    except:
        pat = pat

    # Je récupère les champs de la table formulaire santé
    champsFormulaireSante = [field.name for field in ColSante._meta.get_fields()]
    # Je récupère les ids des lignes de la table formulaire santé
    idDesFormulaires = [valeur.id for valeur in ColSante.objects.all()]
    # Je crée une liste qui contiendra les valeurs des lignes
    # Il y a autant d'élément que de ligne, donc que d'ids récupéré
    # FormulaireSante.objects.filter(id=id).values()[0].values()
    # Dans le code ci-dessus je récupère la ligne ayant un certain id
    # Ensuite je récupère les valeurs de la ligne .values
    # Le 1er élément qui est le dictionnaire des colonnes/valeurs
    # et enfin uniquement les valeurs
    dataFormulaireSante = [ColSante.objects.filter(id=id).values()[0].values() for id in idDesFormulaires]
    dataFormulaireSante_med = pat
    return render(request, "sante_datatable.html",
                  {"dataFormulaireSante" : dataFormulaireSante,
                   "dataFormulaireSante_med" : dataFormulaireSante_med,
                   "champsFormulaireSante" : champsFormulaireSante})

@login_required
def association(request):
    if request.user.role == "patient":
        return redirect ("accueil") #ou autre page disant que fais-tu là
    else:
    #return render (request, "page en question")
    # 1- Récupérer la liste des id des médecins et des patients
    # 2- Ensuite on ne garde que les patients qui ne sont pas dans la table medecinPatient
    # 3- On créé ensuite un template qui contiendra une liste déroulante
    # 4- Dans cette liste déroulante on va afficher d'un côté les médecins
    # et de l'autre les patients filtrés (voir étapge 2)
    # https://developer.mozilla.org/fr/docs/Web/HTML/Element/select
        medecinsID = [medecin for medecin in Utilisateur.objects.filter(role="medecin")]
        patientsID = [patient for patient in Utilisateur.objects.filter(role="patient")]
        listePatientsAssocies = [ligne.idPatient for ligne in medecinPatient.objects.all()]
        listePatientsNonAssocies = [id for id in patientsID if id not in listePatientsAssocies]
        tableAssociation = medecinPatient.objects.all()
        # Syntaxe équivalente
        # for id in patientsID :
        #    if id not in listePatientsAssocies:
        #        patientsNonAssocies.append(id)
        if request.method == "POST":
            medecin_username = request.POST["medecin"]
            patient_username = request.POST["patient"]
            medecin = Utilisateur.objects.get(username=medecin_username)
            patient = Utilisateur.objects.get(username=patient_username)
            print("medecin", type(medecin), medecin)
            medecinPatient(idMedecin=medecin, idPatient=patient).save()
            return redirect("association")
        return render(request, "association.html",
                      {"listePatientsNonAssocies": listePatientsNonAssocies,
                       "medecinsID": medecinsID,
                       "tableAssociation" : tableAssociation})

@login_required
def histo_patient(request):
    champsFormulaireStress = [field.name for field in ColStress._meta.get_fields()]
#    idDesFormulairesStr = [valeur.id for valeur in ColStress.objects.all()]
    idDesFormulairesStr = [valeur.id for valeur in ColStress.objects.filter(user_id=request.user.username)]
    dataFormulaireStress = [ColStress.objects.filter(id=id).values()[0].values() for id in idDesFormulairesStr]

    champsFormulaireSante = [field.name for field in ColSante._meta.get_fields()]
#    idDesFormulairesSante = [valeur.id for valeur in ColSante.objects.all()]
    idDesFormulairesSante = [valeur.id for valeur in ColSante.objects.filter(user_id=request.user.username)]

    dataFormulaireSante = [ColSante.objects.filter(user_id=request.user.username).values()[0].values() for id in idDesFormulairesSante]
    return render(request, "histo_patient.html",
                  {"dataFormulaireSante" : dataFormulaireSante,
                   "champsFormulaireSante" : champsFormulaireSante,
                  "dataFormulaireStress" : dataFormulaireStress,
                   "champsFormulaireStress" : champsFormulaireStress})


#print(list(utilisateur.username for utilisateur in Utilisateur.objects.filter(role="medecin")))

'''
list1 = [utilisateur.username for utilisateur in Utilisateur.objects.filter(role="medecin")]
for utilisateur in Utilisateur.objects.filter(role="patient"):
    if not medecinPatient.objects.filter(idPatient=utilisateur).exists():
        list1.append(utilisateur.username)
print(list1)
'''