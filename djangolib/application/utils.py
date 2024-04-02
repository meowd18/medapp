import random, logging, mlflow
from django.db import connections

logging.basicConfig(level=logging.DEBUG)

def init_mlflow():
    mlflow.set_tracking_uri("sqlite:////home/greta/alternance/medapp/mlflow.db")
    mlflow.set_experiment("database_access_monitoring")


def handle_bug(form, form_name, prenom):
    default_database_settings = connections['default'].settings_dict.copy()
    #définir la connexion default vers la bdd
    with connections['default'].cursor() as cursor:
        #générer un nombre aléatoire pour l'apparition des erreurs
        x = random.randint(1, 100)
        if (x % 2) == 0:
            logging.debug(f'{x}: no bug should arise')
            try:
                form.save()
                logging.debug('insertion successful')
                with mlflow.start_run():
                    mlflow.log_metric("is_insertion_successful", 1)
                    mlflow.log_param("form", form_name)
                    mlflow.log_param("user", prenom)
            except Exception as e:
                logging.debug('insertion failed')
                with mlflow.start_run():
                    mlflow.log_metric("is_insertion_successful", 0)
                    mlflow.log_param("error_message", str(e))
                    mlflow.log_param("form", form_name)
                    mlflow.log_param("user", prenom)
            finally:
                # Restaurer la configuration de la base de données par défaut
                connections['default'].settings_dict = default_database_settings
        else:
            logging.debug(f'{x}: bug inserted')
            #simulation d'une connexion qui pointe vers une mauvaise bdd
            #connections['default'].settings_dict = connections['bddlib'].settings_dict
            try:
                form.using("bddlib").save()
                logging.debug('insertion successful')
                with mlflow.start_run():
                    mlflow.log_metric("is_insertion_successful", 1)
                    mlflow.log_param("form", form_name)
                    mlflow.log_param("user", prenom)
            except Exception as e:
                logging.debug('insertion failed')
                with mlflow.start_run():
                    mlflow.log_metric("is_insertion_successful", 0)
                    mlflow.log_param("error_message", str(e))
                    mlflow.log_param("form", form_name)
                    mlflow.log_param("user", prenom)
            finally:
                # Restaurer la configuration de la base de données par défaut
                connections['default'].settings_dict = default_database_settings
