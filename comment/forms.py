from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Commentaire


class Comform(forms.ModelForm):
    body=forms.CharField(label="",widget=forms.Textarea(attrs={'placeholder':'votre commentaire','rows':4,'cols':100}))
    class Meta:
        model=Commentaire
        fields=('body',)
