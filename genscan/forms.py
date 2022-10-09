from django import forms
from genscan.models import QrCode

def GenerateForm(request):

    class Meta:
        model = QrCode
        fields = ['data']
        
