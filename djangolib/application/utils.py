import random, logging, mlflow, os, sqlite3, requests, traceback
from django.db import connections, OperationalError, reset_queries, close_old_connections
from django.conf import settings
logging.basicConfig(level=logging.DEBUG)

#initialisation de l'expérience sur serveur mlflow
def init_mlflow():
    mlflow.set_tracking_uri("sqlite:////home/greta/alternance/medapp/mlflow.db")
    mlflow.set_experiment("database_access_monitoring")


#serveur discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1194197972859240549/bIM9M48OQjhzfSzbYUz58UF26pUwFAdKRqnutEqSzHzhsEwCPTnqF2NxyQziWeMkHkmc")

#fonction d'envoi de notification sur serveur Discord
def send_alert_discord(subject, body):
    logging.info("alert will be sent")
    try:
        payload = {
            "content": f"**{subject}**\n{body}"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        logging.info('Alert sent successfully.')
    except Exception as e:
        logging.info(f'Error sending Discord alert: {e}')

def check_default_database_existence():
    #vérifier la présence de la bdd à l'endroit spécifié
    db_path = settings.DATABASES['default']['NAME']

    #vérifier si le fichier existe
    if os.path.exists(db_path):
        logging.debug(f"La base de données par défaut existe à l'emplacement: {db_path}")
        return True
    else:
        logging.debug(f"La base de données par défaut n'existe pas à l'emplacement: {db_path}")
        return False

def check_database_connection(cursor):
    #vérifier la connexion à la bdd
    try:
        cursor.execute("SELECT 1")
        logging.debug("La connexion à la base de données fonctionne correctement.")
        return True
    except Exception as e:
        logging.debug("Erreur lors de la connexion à la base de données:", e)
        return False

def handle_bug(form, form_name, prenom):
    #génération d'un nombre aléatoire pour déterminer s'il y aura un bug
    x = random.randint(1, 100)
    bdd = 'default'
    with connections[bdd].cursor() as cursor:
        if (x % 2) == 0:
            logging.debug(f'{x}: no bug should arise')
        else:
            #fermeture de la connexion pour simuler une panne
            logging.debug(f'{x}: bug inserted')
            cursor.connection.close()

    try:
        if not check_default_database_existence(): #si la bdd n'est pas trouvée
            pass #prévenir utilisateur, bloquer formulaires, envoyer alerte
        if not check_database_connection(cursor): #si la connexion est fermée
            #rouvrir la bdd
            reset_queries()
            close_old_connections()
            connections[bdd].ensure_connection()
            logging.debug("La connexion à la base de données a été rétablie avec succès.")
        with connections[bdd].cursor() as cursor:
            form.save()
            logging.debug('insertion successful')
            with mlflow.start_run():
                mlflow.log_metric("is_insertion_successful", 1)
                mlflow.log_param("form", form_name)
                mlflow.log_param("user", prenom)
                message = 'Votre formulaire a bien été enregistré'
                return message
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        logging.debug('insertion failed')
        with mlflow.start_run():
            mlflow.log_metric("is_insertion_successful", 0)
            mlflow.log_param("error_message", str(e))
            mlflow.log_param("form", form_name)
            mlflow.log_param("user", prenom)
            message = "Un problème est survenu lors de l'enregistrement de votre formulaire, veuillez réessayer ultérieurement. Si l'erreur persiste, merci de contacter votre médecin traitant."
            return message

    finally:
        #dans tous les cas, on vérifie le seuil
        #le cas échéant on envoie une alerte discord
        #connexion à la base de données utilisée par MLflow
        conn = sqlite3.connect('/home/greta/alternance/medapp/mlflow.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Récupérer les résultats de la requête
        tables = cursor.fetchall()

        #nombre de valeurs à prendre en compte, ou x dernières valeurs
        metrics = 3
        #seuil d'alerte
        threshold = 2
        #requête SQL pour récupérer toutes les valeurs de métriques
        cursor.execute(f'SELECT value FROM metrics ORDER BY timestamp DESC')
        values = cursor.fetchall()
        #requête SQL pour récupérer les x dernières valeurs
        cursor.execute(f'SELECT value FROM metrics ORDER BY timestamp DESC LIMIT {metrics}')
        x_last_values = cursor.fetchall()
        #requête SQL pour récupérer les messages d'erreur des x derniers échecs
        cursor.execute(f'SELECT params.value FROM params'
                       f' JOIN metrics ON metrics.run_uuid = params.run_uuid'
                       f' WHERE params.key = "error_message" AND metrics.value = 0'
                       f' AND metrics.timestamp IN (SELECT timestamp FROM metrics ORDER BY timestamp DESC LIMIT {metrics})'
                       f' ORDER BY metrics.timestamp DESC')
        x_last_errors = cursor.fetchall()
        #requête SQL pour récupérer les formulaires correspondant aux messages d'erreur
        cursor.execute(f'SELECT params.value FROM params'
                       f' JOIN metrics ON metrics.run_uuid = params.run_uuid'
                       f' WHERE params.key = "form" AND metrics.value = 0 AND metrics.timestamp'
                       f' IN (SELECT timestamp FROM metrics ORDER BY timestamp DESC LIMIT {metrics})'
                       f' ORDER BY metrics.timestamp DESC')
        failed_forms = cursor.fetchall()
        logging.debug(f"x dernières valeurs: {x_last_values}")
        logging.debug(f"x dernières erreurs: {x_last_errors}")
        logging.debug(f"formulaires: {failed_forms}")
        #nombre d'échecs parmi les x dernières valeurs
        fail = sum(val[0] == 0 or val[0] == 0.0 for val in x_last_values)
        logging.debug(f"nombre d'échecs: {fail}")

        # Fermeture de la connexion à la base de données
        conn.close()

        #on vérifie qu'il y a assez de valeurs, que le nombre d'échecs est atteint et que la dernière tentative est un échec
        if len(values) >= metrics and fail >= threshold and x_last_values[0][0] == 0:
            logging.debug('seuil atteint')

            #liste pour stocker les erreurs avec les formulaires associés
            errors_and_forms = []
            unique_errors = set()
            unique_forms = set()

            #parcourir les erreurs récentes et les formulaires associés
            for val, form in zip(x_last_errors, failed_forms):
                error_message = val[0]
                form_name = form[0]

                #vérifier si l'erreur est unique
                if error_message not in unique_errors:
                    errors_and_forms.append({"error": error_message, "forms": {form_name}})
                    unique_errors.add(error_message)
                else:
                    #ajouter le formulaire associé à une erreur existante
                    for entry in errors_and_forms:
                        if entry["error"] == error_message:
                            entry["forms"].add(form_name)

                #ajouter le formulaire associé
                unique_forms.add(form_name)

            #formater les problèmes en une chaîne lisible
            formatted_issues = ""
            counter = 1

            for entry in errors_and_forms:
                error_message = entry["error"]
                forms_associated = ", ".join(entry["forms"])

                formatted_issues += f"\n ⚠️ {counter}. Erreur: {error_message}\n Formulaire(s) associé(s): {forms_associated}\n{'*' * 20}\n"
                counter += 1

            issue = formatted_issues.rstrip('\n') if formatted_issues else "Aucune erreur n'a été trouvée."
            msg = "Echec de l'enregistrement de vos données, veuillez réessayer ultérieurement. Si le problème persiste, contactez votre médecin traitant."
            #générer le message d'alerte pour Discord
            send_alert_discord("Alerte MLflow", f"Le seuil d'échecs ({threshold} envois sur {metrics}) a été atteint."
                  DB                              f"\n Le ou les problèmes suivants ont causé l'alerte: {issue}")