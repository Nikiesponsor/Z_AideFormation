
from os import name
from django import views
from django.urls import path
from .import  views
from .views import  *


app_name= 'programme'

urlpatterns=[
    path('',views.niveau,name='niveau'),
    path('result/x/<int:int_quiz>',views.Resultcorrection,name='resultcorection'),
    path('<int:int_niveau>/matiere',views.matiere,name='matiere'),
    path('<int:int_niveau>/<int:int_matiere>/lecon',views.lecon,name='lecon'),
    path('<int:int_niveau>/<int:int_matiere>/<int:int_lecon>/details',views.datailslecon,name='details'),
    path('<int:int_lecon>/execices',views.exercices,name='exos'),
    path('<int:int_matiere>/listquiz/',views.listquiz,name='listequiz'),
    path('<int:int_matiere>/listquiz/<int:int_quiz>/',views.detail,name='detail'),
    path('correction/<int:int_quiz>',views.correction,name="corect"),
    path('<int:int_matiere>/listquiz/<int:int_quiz>/data',views.dataQuiz,),
    path('<int:int_matiere>/listquiz/<int:int_quiz>/save',views.savequiz,name='save'),
    path('result/quiz',views.resultatQuiz,name='quizresulte'),
    path('resultats/delete/<int:int_quiz>',views.SupQuiz,name='suppquiz'),
    path('general/<int:int_niveau>/',views.genarlquiz,name='GneralListquiz'),
    path('general/<int:int_niveau>/<int:int_quiz>/',views.generalquestion,name='generalquestion'),
    path('general/<int:int_niveau>/<int:int_quiz>/time',views.datatime),
    path('Gcorrection/<int:int_quiz>',views.generalcorrection,name='Generalcorection'),
    path('stat',views.statistique,name='stat'),
    path('genralresultats',views.generalResult,name='generalresultats'),
    path('generalsup/<int:int_quiz>',views.generalSupQuiz,name='generalSupQuiz'),
    path('generaldetailéCorrection/<int:int_quiz>',views.generalresultcorrection,name='generalresultcorrection'),
    path('favoris/<int:int_matiere>',views.favoris,name='favoris_add'),
    path('<int:int_niveau>/matiere/<int:int_matiere>/verification',views.favoris2),
    path('listefavoris/',views.favorilist,name='listefavoris'),
    path('result/quiz/<int:int_quiz>',views.deletajax,),
    path('search/',views.search,name='search'),
    path('fav',views.favorislecon,name='favorislecon'),
    path('favorislecondel/<int:int_lecon>/',views.favorislecondel,name='favorislecondel'),
    path('notifications',views.notifacations,name="notification"),
    path('searchlecon/<int:int_matiere>',views.searchlecon,name='leconsearch')  

]