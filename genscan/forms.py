from django import forms
from genscan.models import QrCode


class GenerateForm(forms.ModelForm):
    class Meta:
        model = QrCode
        fields = "__all__"
        
