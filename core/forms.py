from django import forms
from .models import FormInformation
from.models import Certificate

class FormPreview(forms.ModelForm):
    plan = forms.FileField(
        required = False
    )
    class Meta:
        model = FormInformation
        fields = ['event', 'date', 'body', 'plan']

class Imageform(forms.ModelForm):
    name = forms.ModelChoiceField(Certificate.objects.all(), 
    widget=forms.Select,
    required=False,
    label='Selecione o Certificado'
    )

    class Meta:
        model = Certificate
        fields = ['name']

