ctxt = """Cette application héberge une plateforme de gestion médicale.
Un administrateur attribue des comptes aux médecins, peut consulter l'ensemble des patients inscrits ainsi que l'historique de leurs formulaires dans un tableau avec filtres dynamiques, attribuer des rôles et associer les patients à des médecins.
Les médecins peuvent créer des comptes patients, mais pas les associer à un médecin.
Ils peuvent voir l'historique des formulaires remplis par les patients qui leur sont associés dans un tableau avec filtres dynamiques, et modifier la périodicité à laquelle les patient doivent les remplir.
Les patients remplissent des formulaires avec des informations médicales.
Deux formulaires sont disponibles.
Le premier formulaire concerne des données de santé générales (taille, poids, fréquence cardiaque, symptômes, prise de médicaments, consommation, activité physique).
Par défaut, il doit être rempli tous les jours.
Le second concerne des données sur le stress et doit être rempli, par défaut, tous les 5 jours.
Le patient doit remplir ce formulaire en indiquant, sur une échelle de 0 à 10, la régularité avec laquelle ils ont ressentis les différents symptômes décrits.
Une fois le formulaire rempli, toutes ces notes sont additionnées pour obtenir une note totale de stress sur 440.
L'échelle d'apparition des symptômes de stress est la suivante:
0: Ce symptôme n’est pas apparu au cours des deux dernières semaines
1: Ce symptôme est apparu une ou deux fois seulement au cours des deux dernières semaines
5: Ce symptôme est apparu plusieurs fois au cours des deux dernières semaines
10: Ce symptôme est apparu presque continuellement au cours des deux dernières semaines
Chaque utilisateur peut modifier son mot de passe et ses informations personnelles.
Une suggestion de mot de passe respectant les contraintes de sécurité est proposée au moment de l'inscription et au moment de la modification du mot de passe.
Les contraintes de sécurité sont les suivantes:
La longueur minimale du mot de passe est de 8 caractères.
Il doit contenir au moins une lettre minuscule (a-z).
Il doit contenir au moins une lettre majuscule (A-Z).
Il doit contenir au moins un chiffre (0-9).
Il doit contenir au moins un caractère spécial parmi !@#$%^&*()_+-.
               """