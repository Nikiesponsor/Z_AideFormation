from os import name
from django import views
from django.urls import path
from .import  views
from .views import  *


app_name= 'Quiz'

urlpatterns=[
    path('',views.quiz,name='quiz'),
    path('<int:int_quiz>/',views.questionquiz,name='questionquiz'),
    path('<int:int_quiz>/time',views.datatimes),
    path('jourcorrection/<int:int_quiz>',views.correctionJour,name="jourcorrection"),
    path('jourResultcorrection/<int:int_quiz>',views.ResultcorrectionJour,name="ResultcorrectionJour"),
    path('resultajour',views.resultquizjour,name='resultquizjour'),
    path('supjour/<int:int_quiz>',views.supQuizjour,name='supQuizjour'),
    path('pdf/<int:int_quiz>',views.render_pdf_view,name='pdf'),
    


]