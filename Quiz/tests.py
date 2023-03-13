from django.test import TestCase

# Create your tests here.


from django.shortcuts import render, redirect
from .models import Question, Reponse

def quiz(request):
    if request.method == 'POST':
        # Récupérer toutes les réponses sélectionnées par l'utilisateur
        reponses_utilisateur = request.POST.dict()
        del reponses_utilisateur['csrfmiddlewaretoken']  # supprimer le jeton csrf de la liste des réponses

        # Récupérer toutes les réponses correctes pour chaque question
        reponses_correctes = {}
        for question in Question.objects.all():
            reponses_correctes[question.id] = []
            for reponse in question.reponse_set.all():
                if reponse.est_correcte:
                    reponses_correctes[question.id].append(reponse.id)

        # Comparer les réponses de l'utilisateur aux réponses correctes pour chaque question
        resultat = {'correctes': 0, 'incorrectes': 0}
        for question_id, reponses in reponses_utilisateur.items():
            question_id = int(question_id)
            reponses_utilisateur[question_id] = [int(reponse_id) for reponse_id in reponses]
            if reponses_utilisateur[question_id] == reponses_correctes[question_id]:
                resultat['correctes'] += 1
            else:
                resultat['incorrectes'] += 1

        # Stocker le résultat dans le contexte et afficher le template de résultats
        context = {'resultat': resultat}
        return render(request, 'resultats.html', context)

    else:
        # Afficher toutes les questions et leurs réponses associées
        questions = Question.objects.all()
        context = {'questions': questions}
        return render(request, 'quiz.html', context)
