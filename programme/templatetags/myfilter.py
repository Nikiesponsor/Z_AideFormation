from atexit import register
from os import name
from   django import template
from connex.models import User
from  programme.models import Lecons, Matiere 
register = template.Library()

@register.filter(name='to_char')
def  to_char(value):
    lettre=chr(96+value)
    return  lettre.upper() 

@register.filter(name='index')
def index(sequence,position):
    taille=len(sequence)
    if position < taille:
        id1=sequence[position]
        id=int(id1)
        return id
    else: 
        print("work")

@register.filter(name='check')
def check(int_matiere,int_user):
    matiere=Matiere.objects.get(pk=int_matiere)
    user=User.objects.get(pk=int_user)
    fav=bool
    if matiere.favoris.filter(id=user.id).exists():
        fav=True
    else:
        fav = False
    return fav

@register.filter(name='check2')
def check2(int_lecon,int_user):
    lecon=Lecons.objects.get(pk=int_lecon)
    user=User.objects.get(pk=int_user)
    fav=bool
    if lecon.Favoris.filter(id=user.id).exists():
        fav=True
    else:
        fav=False
    return fav

@register.filter(name='etat')
def etat(etats):
    formes=str(etats)
    return formes

@register.filter(name="veri2")
def veri2(valeur):
    return str(valeur)


