from django.contrib import admin
from .models import Adherant, Historique, PlanAdhesion, Souscription, User

# Register your models here.

admin.site.register(User)
admin.site.register(PlanAdhesion)
admin.site.register(Historique)
admin.site.register(Adherant)
admin.site.register(Souscription)
