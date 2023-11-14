# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(blank=True, null=True, max_length=100)
    email = models.CharField(blank=True, null=True, max_length=50)

    class Meta:
        #managed = False
        db_table = 'users'

class ColStress(models.Model):
    CHOIX = (
        (0, '0'),
        (1, '1'),
        (5, '5'),
        (10, '10'),
    )
    user_id = models.CharField('id Patient', blank=True, null=False, max_length=10)  # The composite primary key (user_id, date) found, that is not supported. The first column is selected.
    date = models.TextField(blank=True, null=True)
    irritabilité = models.IntegerField(choices=CHOIX, blank=True, null=True)
    sentiments_depressifs = models.IntegerField("sentiments dépressifs", choices=CHOIX, blank=True, null=True)
    bouche_seche_ou_gorge_seche = models.IntegerField("bouche ou gorge sèche", choices=CHOIX, blank=True, null=True)
    actions_ou_gestes_impulsifs = models.IntegerField(choices=CHOIX, blank=True, null=True)
    grincement_des_dents = models.IntegerField(choices=CHOIX, blank=True, null=True)
    difficulte_a_rester_assis = models.IntegerField("difficulté à rester assis", choices=CHOIX, blank=True, null=True)
    cauchemars = models.IntegerField(choices=CHOIX, blank=True, null=True)
    diarrhee = models.IntegerField("diarrhée", choices=CHOIX, blank=True, null=True)
    attaques_verbales_envers_quelquun = models.IntegerField("attaques verbales envers quelqu'un", choices=CHOIX, blank=True, null=True)
    hauts_et_bas_emotifs = models.IntegerField("hauts et bas émotifs", choices=CHOIX, blank=True, null=True)
    grande_envie_de_pleurer = models.IntegerField(choices=CHOIX, blank=True, null=True)
    grande_envie_de_fuir = models.IntegerField(choices=CHOIX, blank=True, null=True)
    grande_envie_de_faire_mal = models.IntegerField(choices=CHOIX, blank=True, null=True)
    pensees_embrouillees = models.IntegerField("pensées embrouillées", choices=CHOIX, blank=True, null=True)
    debit_plus_rapide = models.IntegerField("débit plus rapide", choices=CHOIX, blank=True, null=True)
    fatigue_ou_lourdeur_generalisees = models.IntegerField("fatigue ou lourdeur généralisée", choices=CHOIX, blank=True, null=True)
    sentiment_detre_surchargee = models.IntegerField("sentiment d'être surchargé.e", choices=CHOIX, blank=True, null=True)
    sentiment_detre_emotivement_fragile = models.IntegerField("sentiment d'être émotivement fragile", choices=CHOIX, blank=True, null=True)
    sentiment_de_tristesse = models.IntegerField(choices=CHOIX, blank=True, null=True)
    sentiment_danxiete = models.IntegerField("sentiment d'anxiété", choices=CHOIX, blank=True, null=True)
    tension_emotionnelle = models.IntegerField("tension émotionnelle", choices=CHOIX, blank=True, null=True)
    hostilite_envers_les_autres = models.IntegerField("hostilité envers les autres", choices=CHOIX, blank=True, null=True)
    tremblements_ou_gestes_nerveux = models.IntegerField(choices=CHOIX, blank=True, null=True)
    begaiements_ou_hesitations_verbales = models.IntegerField("bégaiements ou hésitations verables", choices=CHOIX, blank=True, null=True)
    incapacite_ou_difficulte_a_se_concentrer = models.IntegerField("incapacité ou difficulté à se concentrer", choices=CHOIX, blank=True, null=True)
    difficulte_a_organiser_ses_pensees = models.IntegerField("difficulté à organiser ses pensées", choices=CHOIX, blank=True, null=True)
    difficulte_a_dormir_toute_la_nuit_sans_se_reveiller = models.IntegerField("difficulté à dormir toute la nuit sans se réveiller", choices=CHOIX, blank=True, null=True)
    besoin_frequent_duriner = models.IntegerField("besoin fréquent d'uriner", choices=CHOIX, blank=True, null=True)
    maux_destomac_ou_difficultes_a_digerer = models.IntegerField("maux d'estomac ou difficultés à digérer", choices=CHOIX, blank=True, null=True)
    geste_ou_sentiment_dimpatience = models.IntegerField("geste ou sentiment d'impatience", choices=CHOIX, blank=True, null=True)
    maux_de_tete = models.IntegerField("maux de tête", choices=CHOIX, blank=True, null=True)
    douleurs_au_dos_ou_a_la_nuque = models.IntegerField(choices=CHOIX, blank=True, null=True)
    perte_ou_gain_dappetit = models.IntegerField("perte ou gain d'appétit", choices=CHOIX, blank=True, null=True)
    perte_dinteret_pour_le_sexe = models.IntegerField("perte d'intérêt pour le sexe", choices=CHOIX, blank=True, null=True)
    oublis_frequents = models.IntegerField("oublis fréquents", choices=CHOIX, blank=True, null=True)
    douleurs_ou_serrements_a_la_poitrine = models.IntegerField(choices=CHOIX, blank=True, null=True)
    conflits_significatifs_avec_les_autres = models.IntegerField(choices=CHOIX, blank=True, null=True)
    difficultes_a_se_lever_apres_le_sommeil = models.IntegerField("difficulté à se lever après le sommeil", choices=CHOIX, blank=True, null=True)
    sentiment_que_les_choses_sont_hors_de_controle = models.IntegerField("sentiment que les choses sont hors de contrôle", choices=CHOIX, blank=True, null=True)
    difficulte_a_faire_une_longue_activite_continue = models.IntegerField("difficultés à faire une longue activité continue", choices=CHOIX, blank=True, null=True)
    mouvements_de_retrait_disolement = models.IntegerField("mouvements de retrait, d'isolement", choices=CHOIX, blank=True, null=True)
    difficulte_a_sendormir = models.IntegerField("difficulté à s'endormir", choices=CHOIX, blank=True, null=True)
    difficulte_a_se_remettre_dun_evenement_contrariant = models.IntegerField("difficulté à se remettre d'un évènement", choices=CHOIX, blank=True, null=True)
    mains_moites = models.IntegerField(choices=CHOIX, blank=True, null=True)
    total_de_limpact_du_stress_dans_votre_vie_actuelle = models.IntegerField()
    #total_de_limpact_du_stress_dans_votre_vie_actuelle = models.IntegerField("total de l'impact du stress dans votre vie actuelle", blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'col_stress'

class ColSante(models.Model):
    user_id = models.CharField("id Patient", blank=True, null=False, max_length=10)  # The composite primary key (user_id, date) found, that is not supported. The first column is selected.
    date = models.TextField(blank=True, null=True)
    poids = models.IntegerField("poids en kg", blank=True, null=True)
    tour_de_taille_en_cm = models.IntegerField(blank=True, null=True)
    fréquence_cardiaque_par_minute = models.IntegerField(blank=True, null=True)
    tension_artérielle_systolique_prise_du_matin = models.IntegerField(blank=True, null=True)
    tension_artérielle_systolique_prise_du_soir = models.IntegerField(blank=True, null=True)
    tension_artérielle_diastolique_prise_du_matin = models.IntegerField(blank=True, null=True)
    tension_artérielle_diastolique_prise_du_soir = models.IntegerField(blank=True, null=True)
    symptomes_cardiovasculaires_en_quelques_mots = models.CharField("symptômes cardiovasculaires en quelques mots", blank=True, null=True, max_length=150)
    nombre_de_médicaments_pris_dans_la_journée = models.IntegerField(blank=True, null=True)
    oubli_de_prendre_les_médicaments_le_matin = models.BooleanField(blank=True, null=True)
    oubli_de_prendre_les_médicaments_le_soir = models.BooleanField(blank=True, null=True)
    effets_secondaires_remarqués = models.BooleanField(blank=True, null=True)
    symptomes_particuliers_remarqués = models.BooleanField("symptômes particuliers remarqués", blank=True, null=True)
    effets_secondaires_et_ou_symptomes_particuliers_en_quelques_mots = models.CharField("effets secondaires et/ou symptômes particuliers en quelques mots", blank=True, null=True, max_length=150)
    consommation_dalcool = models.BooleanField("consommation d'alcool", blank=True, null=True)
    grignotage_sucre = models.BooleanField("grignotage sucré", blank=True, null=True)
    grignotage_sale = models.BooleanField("grignotage salé", blank=True, null=True)
    nombre_de_repas_pris_durant_la_journée = models.IntegerField(blank=True, null=True)
    quantité_deau_bue_en_litre = models.FloatField("quantité d'eau bue en litres", blank=True, null=True)
    quantité_dalcool_consommé_en_litre = models.FloatField("quantité d'alcool consommé en litres", blank=True, null=True)
    activité_physique_aujourdhui = models.BooleanField("activité physique aujourd'hui", blank=True, null=True)
    nature_de_votre_activité_physique = models.CharField(blank=True, null=True, max_length=150)
    durée_de_lactivité_physique_en_minutes = models.IntegerField("durée de l'activité physiques en minutes", blank=True, null=True)
    présence_de_dyspnée = models.BooleanField(blank=True, null=True)
    présence_dœdème = models.BooleanField("présence d'œdème", blank=True, null=True)
    présence_dépisode_infectieux = models.BooleanField("présence d'épisode infectieux", blank=True, null=True)
    présence_de_fièvre = models.BooleanField(blank=True, null=True)
    présence_de_palpitation = models.BooleanField(blank=True, null=True)
    présence_de_douleur_thoracique = models.BooleanField(blank=True, null=True)
    présence_de_malaise = models.BooleanField(blank=True, null=True)
    heure_de_début_des_palpitations = models.TimeField("début des palpitations (format HH:MM:SS)", blank=True, null=True)
    durée_totale_des_palpitations_en_minutes = models.IntegerField(blank=True, null=True)
    heure_de_début_des_douleurs_thoraciques = models.TimeField("début des douleurs thoraciques (format HH:MM:SS)", blank=True, null=True)
    durée_totale_des_douleurs_thoraciques_en_minutes = models.IntegerField(blank=True, null=True)
    heure_de_début_des_malaises = models.TimeField("début des malaises (format HH:MM:SS)", blank=True, null=True)
    durée_totale_des_malaises_en_minutes = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'col_sante'

    def validate_duree(self, presence, duree_champ, message_prefix):
        if presence and duree_champ == 0:
            raise ValidationError(f"Si vous indiquez {message_prefix}, veuillez spécifier une durée supérieure à zéro.")
        elif not presence and duree_champ != 0:
            raise ValidationError(f"Si vous n'indiquez pas {message_prefix}, la durée doit être égale à zéro.")

    def clean(self):
        # Appeler la méthode clean du modèle de base pour exécuter les validations par défaut
        super().clean()

        # Consommation alcool
        if self.consommation_dalcool and self.quantité_dalcool_consommé_en_litre == 0:
            raise ValidationError("Si vous indiquez une consommation d'alcool, veuillez spécifier une quantité d'alcool supérieure à zéro.")
        elif not self.consommation_dalcool and self.quantité_dalcool_consommé_en_litre != 0:
            raise ValidationError("Si vous n'indiquez pas de consommation d'alcool, la quantité d'alcool consommée doit être égale à zéro.")

        # Activité physique
        self.validate_duree(self.activité_physique_aujourdhui, self.durée_de_lactivité_physique_en_minutes, "une activité physique")

        # Palpitations
        self.validate_duree(self.présence_de_palpitation, self.durée_totale_des_palpitations_en_minutes, "des palpitations")

        # Douleurs thoraciques
        self.validate_duree(self.présence_de_douleur_thoracique, self.durée_totale_des_douleurs_thoraciques_en_minutes, "des douleurs thoraciques")

        # Malaises
        self.validate_duree(self.présence_de_malaise, self.durée_totale_des_malaises_en_minutes, "des malaises")