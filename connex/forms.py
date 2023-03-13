from dataclasses import fields
import email
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    email= forms.CharField(label='Non d utilisateur',widget=forms.TextInput(attrs={'class':"",'placeholder':"Email",}))
    password= forms.CharField(label='mots de passe',widget=forms.PasswordInput(attrs={'class':'password','placeholder':"Mot de passe",}))

class ReqisterForm(UserCreationForm):
    email= forms.CharField(label='Email',widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    last_name=forms.CharField(label='Nom',widget=forms.TextInput(attrs={'placeholder':'Nom'}))
    first_name=forms.CharField(label='Prenom',widget=forms.TextInput(attrs={'placeholder':'Prénom'}))
    # telphone=PhoneNumberField(label='Telephone',widget=forms.NumberInput(attrs={'placeholder':'70 01 01 00','type':'tel'}))
    password1= forms.CharField(label='Mots de passe',widget=forms.PasswordInput(attrs={'placeholder':'Mot de passe','class':'password'}))
    password2= forms.CharField(label='comfirmer votre mots de passe',widget=forms.PasswordInput(attrs={'placeholder':'Confirmer mot de passe','class':'password'}))
    ceckbox_info=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'required'}))
    class Meta:
        model = User
        fields=('email','first_name','last_name','password1','password2','ceckbox_info',)


class ChangepasswordForm(PasswordChangeForm):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Encien mot de passe'}))
    new_password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Nouveau mot de passe'}))
    new_password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Confirmer mot de passe'}))

class ResetpasswordForm(SetPasswordForm):
    new_password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Nouveau mot de passe'}))
    new_password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'password','placeholder':'Confirmer mot de passe'}))



class Resetform(PasswordResetForm):
    email= forms.CharField(label='Email',widget=forms.EmailInput(attrs={'placeholder':'E-mail'}))
    class Meta:
        models=User
        fields=('email')
    

class ProfileForm(forms.Form):
    nom=forms.CharField(widget=forms.TextInput(attrs={'placeholder':''}))
    prenom=forms.CharField(widget=forms.TextInput(attrs={'placeholder':''}))
    telephone=PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':'','type':'tel'}))

