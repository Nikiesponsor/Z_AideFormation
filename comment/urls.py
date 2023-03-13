from django.urls  import path
from .import views

app_name='comment'

urlpatterns=[
    path('',views.info,name="info"),
    path('<int:int_inf>/commentaire',views.commentaire,name='comment'),
    path('<int:int_com>/delete',views.deletcom,name="delete"),
]