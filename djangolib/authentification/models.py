from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#trop long, la flemme
'''class Connexion(models.Model):
    username = models.CharField(max_length=50)
    mdp = models.CharField(max_length=50)'''

class Utilisateur(AbstractUser):
    pass


