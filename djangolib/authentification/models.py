from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#trop long, la flemme
'''class Connexion(models.Model):
    username = models.CharField(max_length=50)
    mdp = models.CharField(max_length=50)'''

class Utilisateur(AbstractUser):
    #patient = 'patient'
    #medecin = 'medecin'
    #responsable = 'responsable'

    lesRoles = {
        ('patient', 'patient'),
        ('medecin', 'medecin'),
        ('responsable', 'responsable'),
    }
    role = models.CharField(max_length=30,
                                   choices=lesRoles,
                                   verbose_name='Rôle', null=True)



class medecinPatient(models.Model):
    idPatient = models.ForeignKey(Utilisateur, null=True, on_delete=models.CASCADE, related_name="patientMedecin", unique=True)
    idMedecin = models.ForeignKey(Utilisateur, null=True, on_delete=models.CASCADE, related_name="medecinPatient")
    #idPatient = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="patientMedecin")
    #idMedecin = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="medecinPatient")


