import random, logging
from django.db import connections
logging.basicConfig(level=logging.DEBUG)

def add_bug():
    #définir la connexion default vers la bdd
    with connections['default'].cursor() as cursor:
        #générer un nombre aléatoire pour l'apparition des erreurs
        x = random.randint(1, 100)
        if (x % 2) == 0:
            logging.debug(f'{x}: no bug should arise')
        else:
            logging.debug(f'{x}: bug inserted')
            #simulation d'une connexion qui pointe vers une mauvaise bdd
            connections['default'].settings_dict = connections['bddlib'].settings_dict

