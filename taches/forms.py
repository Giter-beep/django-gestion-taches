from django import forms
from .models import Intervenant, Client, Intervention

class IntervenantForm(forms.ModelForm):
    class Meta:
        model = Intervenant
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = '__all__'
