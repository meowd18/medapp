from django import forms
from .models import Utilisateur


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ["first_name", "last_name", "email"]

class ModificationMDPForm(forms.Form):
    regexMDP = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-]).{8,}$"
    ancienMDP = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    nouveauMDP1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'pattern': regexMDP}),
        label="Nouveau mot de passe",
        required=True
    )
    nouveauMDP2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le nouveau mot de passe", required=True)
