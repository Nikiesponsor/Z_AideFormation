from django.contrib import admin
from .models import *

# Register your models here.


class Reponse(admin.TabularInline):
    model= Reponsesjour

@admin.register(Questionsjour)
class GenericAdmin(admin.ModelAdmin):
    inlines=(Reponse,)


admin.site.register(Quizjour)
admin.site.register(Reponsesjour)
admin.site.register(Resultasjour)