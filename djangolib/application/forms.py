from django import forms
from django.db import models
from .models import ColStress, ColSante

class ColStressForm(forms.ModelForm):
    class Meta:
        model = ColStress
        exclude = ['total_de_limpact_du_stress_dans_votre_vie_actuelle']

    def __init__(self, *args, **kwargs):
        super(ColStressForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        if 'prénom' in initial:
            self.initial['user_id'] = initial['prénom']


class ColSanteForm(forms.ModelForm):
    class Meta:
        model = ColSante
        fields = '__all__'

        widgets = {
            field.name: forms.NumberInput(attrs={'min': 0})
            for field in ColSante._meta.get_fields()
            if isinstance(field, (forms.IntegerField, models.IntegerField)) and field.name != 'id'
        }

    def __init__(self, *args, **kwargs):
        super(ColSanteForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        if 'prénom' in initial:
            self.initial['user_id'] = initial['prénom']