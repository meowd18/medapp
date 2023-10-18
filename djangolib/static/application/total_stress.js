function updateTotalDeLimpact() {
    var total = 0;

    var fieldsToCalculate = [
        'irritabilité',
        'sentiments dépressifs',
        'bouche ou gorge sèche',
        'actions_ou_gestes_impulsifs',
        'grincement_des_dents',
        'difficulte_a_rester_assis',
        'cauchemars',
        'diarrhee',
        'attaques_verbales_envers_quelquun',
        'hauts_et_bas_emotifs',
        'grande_envie_de_pleurer',
        'grande_envie_de_fuir',
        'grande_envie_de_faire_mal',
        'pensees_embrouillees',
        'debit_plus_rapide',
        'fatigue_ou_lourdeur_generalisees',
        'sentiment_detre_surchargee',
        'sentiment_detre_emotivement_fragile',
        'sentiment_de_tristesse',
        'sentiment_danxiete',
        'tension_emotionnelle',
        'hostilite_envers_les_autres',
        'tremblements_ou_gestes_nerveux',
        'begaiements_ou_hesitations_verbales',
        'incapacite_ou_difficulte_a_se_concentrer',
        'difficulte_a_organiser_ses_pensees',
        'difficulte_a_dormir_toute_la_nuit_sans_se_reveiller',
        // Ajoutez d'autres champs ici
    ];

    for (var i = 0; i < fieldsToCalculate.length; i++) {
        var fieldName = fieldsToCalculate[i];
        var fieldValue = parseInt(document.getElementById('id_' + fieldName).value);
        total += isNaN(fieldValue) ? 0 : fieldValue;
    }

    document.getElementById('id_total_de_limpact_du_stress_dans_votre_vie_actuelle').value = total;
}

// Ajoutez des écouteurs d'événements pour chaque champ à surveiller
for (var i = 0; i < fieldsToCalculate.length; i++) {
    var fieldName = fieldsToCalculate[i];
    var fieldElement = document.getElementById('id_' + fieldName);
    fieldElement.addEventListener('input', updateTotalDeLimpact);
}

// Appelez updateTotalDeLimpact pour calculer le total initial
updateTotalDeLimpact();
