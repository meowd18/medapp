from django import forms
from django.db import models
from .models import ColStress, ColSante

class ColStressForm(forms.ModelForm):
    class Meta:
        model = ColStress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ColStressForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        if 'prénom' in initial:
            self.initial['user_id'] = initial['prénom']

class ColSanteForm(forms.ModelForm):
    class Meta:
        model = ColSante
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ColSanteForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        if 'prénom' in initial:
            self.initial['user_id'] = initial['prénom']