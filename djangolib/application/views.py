from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ColStressForm, ColSanteForm
from .models import ColSante, ColStress
from authentification.models import Utilisateur, medecinPatient
from datetime import datetime, date, timedelta
from django.http import HttpResponseBadRequest
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
def data_stress(request, prochainFormulaire_date_stress=None):
    message = ""
    disabled = ""
    dateDernierFormulaireDuPatient = list(ColStress.objects.filter(user_id=Utilisateur.objects.filter(username=request.user.username)[0]))[-1].date
    dateDernierFormulaireDuPatient = datetime.strptime(dateDernierFormulaireDuPatient, '%d/%m/%Y')
    medecinTraitant = medecinPatient.objects.filter(idPatient=Utilisateur.objects.filter(username=request.user.username)[0].id)[0].idMedecin
    periodiciteMedecin = Utilisateur.objects.filter(username=medecinTraitant)[0].periodiciteStress
    prochainFormulaire = dateDernierFormulaireDuPatient + timedelta(days=periodiciteMedecin)
    prochainFormulaire = prochainFormulaire.strftime('%d/%m/%Y')

    # Convert prochainFormulaire_str back to datetime.date
    prochainFormulaire_date_stress = datetime.strptime(prochainFormulaire, '%d/%m/%Y').date()
    remplirProchainFormulaire = datetime.now().date() > prochainFormulaire_date_stress

    if request.user.role != "patient":
        return redirect("accueil")
    else:
        prenom = request.user.username
        initial_data = {'prénom': prenom}
        initial_data['date'] = date.today().strftime('%d/%m/%Y')

        if request.method == 'POST':
            form = ColStressForm(request.POST, initial=initial_data)
            if form.is_valid() and remplirProchainFormulaire:
                form.save()
                return redirect('accueil')  # Redirect to a confirmation page
            elif not remplirProchainFormulaire:
                message = "Vous ne pouvez pas encore soumettre de réponse pour ce questionnaire"
        else:
            form = ColStressForm(initial=initial_data)

    return render(
        request,
        'data_stress.html',
        {'form': form, 'prochainFormulaire_date_stress': prochainFormulaire_date_stress, 'message': message}
    )



@login_required
def data_sante(request, prochainFormulaire_date_sante=None):
    message = ""
    disabled = ""
    dateDernierFormulaireDuPatient = list(ColSante.objects.filter(user_id=Utilisateur.objects.filter(username=request.user.username)[0]))[-1].date
    dateDernierFormulaireDuPatient = datetime.strptime(dateDernierFormulaireDuPatient, '%d/%m/%Y')
    medecinTraitant = medecinPatient.objects.filter(idPatient=Utilisateur.objects.filter(username=request.user.username)[0].id)[0].idMedecin
    periodiciteMedecin = Utilisateur.objects.filter(username=medecinTraitant)[0].periodiciteSante
    prochainFormulaire = dateDernierFormulaireDuPatient + timedelta(days=periodiciteMedecin)
    prochainFormulaire = prochainFormulaire.strftime('%d/%m/%Y')

    # Convert prochainFormulaire_str back to datetime.date
    prochainFormulaire_date_sante = datetime.strptime(prochainFormulaire, '%d/%m/%Y').date()
    remplirProchainFormulaire = datetime.now().date() > prochainFormulaire_date_sante

    if request.user.role != "patient":
        return redirect("accueil")
    else:
        prenom = request.user.username
        initial_data = {'prénom': prenom}
        initial_data['date'] = date.today().strftime('%d/%m/%Y')

        if request.method == 'POST':
            form = ColSanteForm(request.POST, initial=initial_data)
            if form.is_valid() and remplirProchainFormulaire:
                form.save()
                return redirect('accueil')  # Redirect to a confirmation page
            elif not remplirProchainFormulaire:
                message = "Vous ne pouvez pas encore soumettre de réponse pour ce questionnaire"
        else:
            form = ColSanteForm(initial=initial_data)

    return render(
        request,
        'data_sante.html',
        {'form': form, 'prochainFormulaire_date_sante': prochainFormulaire_date_sante, 'message': message}
    )


#interdire accès à une page en fonction du rôle
'''if request.user.role != "medecin":
    return redirect ("accueil") #ou autre page disant que fais-tu là
else:
    return render (request, "page en question")'''

@login_required
def stress_datatable(request):
    user = request.user
    pat = []

    if request.method == "POST":
        periodiciteStress = request.POST.get("periodiciteStress")

        # Update periodicity for the connected user
        Utilisateur.objects.filter(id=user.id).update(
            periodiciteStress=periodiciteStress
        )

    # Fetch updated periodicity values
    user.refresh_from_db()
    periodiciteStress = user.periodiciteStress

    if user.role == "responsable":
        idDesFormulaires = [valeur.id for valeur in ColStress.objects.all()]
        dataFormulaireStress = [ColStress.objects.filter(id=id).values()[0].values() for id in idDesFormulaires]
    elif user.role == "medecin":
        for p in medecinPatient.objects.filter(idMedecin=user.id).values():
            username_pat = Utilisateur.objects.get(id=p["idPatient_id"]).username
            dataFormulaireStress = [el.values() for el in ColStress.objects.filter(user_id=username_pat).values()]
            pat.extend(dataFormulaireStress)

    champsFormulaireStress = [field.name for field in ColStress._meta.get_fields()]

    return render(request, "stress_datatable.html", {
        "dataFormulaireStress": pat if user.role == "medecin" else dataFormulaireStress,
        "champsFormulaireStress": champsFormulaireStress,
        "periodiciteStress": periodiciteStress
    })



@login_required
def sante_datatable(request):
    user = request.user
    pat = []

    if request.method == "POST":
        periodiciteSante = request.POST.get("periodiciteSante")

        # Update periodicity for the connected user
        Utilisateur.objects.filter(id=user.id).update(
            periodiciteSante=periodiciteSante
        )

    # Fetch updated periodicity values
    user.refresh_from_db()
    periodiciteSante = user.periodiciteSante

    if user.role == "responsable":
        idDesFormulaires = [valeur.id for valeur in ColSante.objects.all()]
        dataFormulaireSante = [ColSante.objects.filter(id=id).values()[0].values() for id in idDesFormulaires]
    elif user.role == "medecin":
        for p in medecinPatient.objects.filter(idMedecin=user.id).values():
            username_pat = Utilisateur.objects.get(id=p["idPatient_id"]).username
            dataFormulaireSante = [el.values() for el in ColSante.objects.filter(user_id=username_pat).values()]
            pat.extend(dataFormulaireSante)

    champsFormulaireSante = [field.name for field in ColSante._meta.get_fields()]

    return render(request, "sante_datatable.html", {
        "dataFormulaireSante": pat if user.role == "medecin" else dataFormulaireSante,
        "champsFormulaireSante": champsFormulaireSante,
        "periodiciteSante": periodiciteSante
    })

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


@login_required
def edaia(request):
    # URL de l'image externe
    image_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Under_construction_graphic.gif"
    # Passer l'URL à la template
    context = {
        'image_url': image_url,
    }
    return render(request, 'edaia.html', context)


#print(list(utilisateur.username for utilisateur in Utilisateur.objects.filter(role="medecin")))

'''
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
'''