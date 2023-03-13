from django.contrib import admin
from .models import  *

# Register your models here.



class Matiereinlines(admin.TabularInline):
    model= Matiere

class Leconinlines(admin.TabularInline):
    model= Lecons

class Exercicesinlines(admin.TabularInline):
    model= Exercices

class Reponse_inlines(admin.TabularInline):
    model= ReponsesQUiz


@admin.register(Niveau)
class GenericAdmin(admin.ModelAdmin):
    inlines=(Matiereinlines,)

@admin.register(Matiere)
class GenericAdmin(admin.ModelAdmin):
    #inlines=(Leconinlines,)
    list_filter=("matiere_niveau",)


@admin.register(Lecons)
class GenericAdmin(admin.ModelAdmin):
    #inlines=(Exercicesinlines,Videoinlines,)
    list_filter=("lecon_niveau","lecon_matiere",)


@admin.register(Exercices)
class GenericAdmin(admin.ModelAdmin):
    list_filter=("exercices_niveau","exercices_matiere","exercices_lecons",)


@admin.register(QuestionQuiz)
class GenericAdmin(admin.ModelAdmin):
    inlines=(Reponse_inlines,)
    

admin.site.register(Quiz)
admin.site.register(ReponsesQUiz)
admin.site.register(Resultats)



##############General################

class GReponse(admin.TabularInline):
    model= GeneralReponses

@admin.register(GeneralQuestion)
class GenericAdmin(admin.ModelAdmin):
    inlines=(GReponse,)


admin.site.register(Generalquiz)
admin.site.register(GeneralReponses)
admin.site.register(GeneralResultats)

