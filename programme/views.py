
from ast import Return
from atexit import register
from cgitb import html, text
from tabnanny import check
from django.shortcuts import redirect, render
from django.template import context
from .models import GeneralQuestion, GeneralReponses, GeneralResultats, Generalquiz, Niveau, Lecons, Matiere, Exercices,Quiz,QuestionQuiz,Resultats,ReponsesQUiz
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse,Http404,HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib import messages
from connex.models import Adherant, Souscription
from django.template.defaulttags import register 
from django.conf import settings
import  os
from Quiz.models import *
import datetime
from datetime import timedelta
from datetime import datetime as dt
aujourdhui = datetime.date.today()
import random
from django.shortcuts import render, get_object_or_404



# Create your views here.
# @login_required(login_url='connex:log')
def niveau(request):
    niveau=Niveau.objects.all()
    return render(request,'niveau.html',{'niveaus':niveau})

#@login_required(login_url='connex:log')
def matiere(request,int_niveau):
    niv=Niveau.objects.all()
    niveau=Niveau.objects.get(pk=int_niveau)
    # niveau=get_object_or_404(Niveau,int_niveau)
    matiere=niveau.matiere.all()
    context={
        'matieres':matiere,
        'niveau':niveau,
        'nivs':niv
        }             
    return render(request,'matiere.html',context)


# @login_required(login_url='connex:log')
def lecon(request,int_niveau,int_matiere):
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    matiere=Matiere.objects.get(pk=int_matiere)
    # matiere=get_object_or_404(Matiere,int_matiere)
    lecon=matiere.lecon.all()
    search=request.GET.get('search')
    if search !='' and search is not None:
        lecon=matiere.lecon.filter(Nom_lecon__icontains=search)
    return render(request,'lecon.html',{'lecons':lecon,'matiere':matiere,'color':color})

# @login_required(login_url='connex:log')
def datailslecon(request,int_niveau,int_matiere,int_lecon):
    matiere=Matiere.objects.get(pk=int_matiere)
    lecon=matiere.lecon.all()
    details=Lecons.objects.get(pk=int_lecon)
    # details=get_object_or_404(Lecons,int_lecon)
    ok=bool
    if details.lecon_pdf:
        ok=True
        ok=str(ok)
    else:
        ok=False
        ok=str(ok)
    # if request.user.is_authenticated :
    #     check1=Adherant.objects.get(user=request.user)
    #     check2=Souscription.objects.filter(adherant_souscrit=check1).exists()
    #     check=str(check2)
    # else:
    #     check='False' 
    context={
        'details':details,
        # 'check':check,
        'lecons':lecon,
        'ok':ok
    }
    return render(request,'detailslecon.html',context)

# @login_required(login_url='connex:log')
def exercices(request,int_lecon):
    lecon=Lecons.objects.get(pk=int_lecon)
    # lecon=get_object_or_404(Lecons,int_lecon)
    exercices=lecon.exercices.all()
    # check1=Adherant.objects.get(user=request.user)
    # check2=Souscription.objects.filter(adherant_souscrit=check1).exists()
    # if check2== False:
    #     messages.error(request,'Veuillez vous Abonnez pour voir la correction')
    #     return redirect('connex:plan')
    context={
        'exos':exercices,
        'lecon':lecon
    }
    return render(request,'exercices.html',context)


def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response=HttpResponse(fh.read(),content_type="application/lecon_pdf")
            response['content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404

@login_required(login_url='connex:log')
def listquiz(request,int_matiere):
    matiere=Matiere.objects.get(pk=int_matiere)
    # matiere=get_object_or_404(Matiere,int_matiere)
    quiz=matiere.QuizMatiere.all()
    nombre=Resultats.objects.filter(user=request.user).count()
    nombre=int(nombre)
    fav=bool
    if quiz :
        fav= True
        fav=str(fav)
    else :
        fav=False
        fav=str(fav)

    context={
        'quizs':quiz,
        'matiere': matiere,
        'fav':fav,
        'nombre':nombre
    }
    return render(request,'listequiz.html',context)

@login_required(login_url='connex:log')
def detail(request,int_matiere,int_quiz):
    matiere=Matiere.objects.get(pk=int_matiere)
    details=Quiz.objects.get(pk=int_quiz)
    score= None
    jouer = details.quizmodule.filter(user=request.user).exists()
    if jouer == True:
        score = details.quizmodule.filter(user=request.user).first()
        score= int(score.score)
    compte=1
    context={
        'lecon':lecon,
        'details':details,
        'compte':compte,
        'score':score,
        'jouer':jouer,
    }
    return render(request,"questionquiz2.html",context)

@login_required(login_url='connex:log')
def correction(request,int_quiz):
    if request.method== 'POST':
        print(request.POST)
        data=request.POST      
        data_=dict(data)        
        data_.pop('csrfmiddlewaretoken')
        questions=[]
        for  k in data_.keys():
            question=QuestionQuiz.objects.get(text=k)
            questions.append(question)
        user= request.user 
        quiz= Quiz.objects.get(pk=int_quiz)
        scrore =0
        mutiplier = 100/ quiz.nombreDequestion
        results=[] 
        correctreponse= None
        for q in questions:               
            reponse_selectionner= request.POST.get(q.text)
            if reponse_selectionner !="":
                questionAns= ReponsesQUiz.objects.filter(question=q)
                for reponse in questionAns:
                    if reponse_selectionner ==  reponse.text:
                        if reponse.correct:
                            scrore +=1
                            correctreponse = reponse.text
                    else:
                        if reponse.correct:
                            correctreponse = reponse.text 
                
                results.append({str(q): {'reponse_correct':correctreponse, 'reponseselect':reponse_selectionner}  }) 
            else:
                results.append({str(q): 'pas de reponse'})
        check1=Adherant.objects.get(user=request.user)
        check2=Souscription.objects.filter(adherant_souscrit=check1).exists()
        if check2== False:
            messages.error(request,'Veuillez vous Abonnez pour voir la correction')
            return redirect('connex:plan')
        score_= scrore * mutiplier
        Resultats.objects.create(quiz=quiz,user=user,score=score_)
        results_={}
        for re in results:
            results_.update(re)        
        if score_>= quiz.score:
            context={'test':True, 'score':score_,'resultat':results_,'quiz':quiz }
            return render(request,'correction.html',context)            
        else: 
            context={'test':False, 'score':score_,'resultat':results_,'quiz':quiz }
            return render(request,'correction.html',context)

    
@login_required(login_url='connex:log')
def dataQuiz(request,int_matiere,int_quiz):
    quiz=Quiz.objects.get(pk=int_quiz)
    questions=[]
    for q in quiz.get_question():
        reponses=[]
        for a in q.get_reponse():
            reponses.append(a.text)
        questions.append({ str(q):reponses})    
    return JsonResponse(
        {'data':questions,
         'temps':quiz.temps})

@login_required(login_url='connex:log')
def savequiz(request,int_matiere,int_quiz):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        questions=[]
        data= request.POST
        data_=dict(data.lists()) 
        data_.pop('csrfmiddlewaretoken')
        print(data_)
        
        for k in data_.keys():
            # data_.keys  toutes les question recues
            question =QuestionQuiz.objects.get(text=k)
            questions.append(question)
        user= request.user 
        quiz= Quiz.objects.get(pk=int_quiz)
        scrore =0
        mutiplier = 100/ quiz.nombreDequestion
        results=[] 
        correctreponse= None
        for q in questions:           
            reponse_selectionner= request.POST.get(q.text)
            if reponse_selectionner !="":
                questionAns= ReponsesQUiz.objects.filter(question=q)
                for reponse in questionAns:
                    if reponse_selectionner ==  reponse.text:
                        if reponse.correct:
                            scrore +=1
                            correctreponse = reponse.text
                    else:
                        if reponse.correct:
                            correctreponse = reponse.text 
                
                results.append({str(q): {'reponse_correct':correctreponse, 'reponseselect':reponse_selectionner}  }) 
            else:
                results.append({str(q): 'pas de reponse'}) 
        score_= scrore * mutiplier
        Resultats.objects.create(quiz=quiz,user=user,score=score_)
        
        
        if score_>= quiz.score:
            context={'test':True, 'score':score_,'resultat':results }
            return JsonResponse({'html': render_to_string('correction.html',context,request=request)})
            
        else: 
            context={'test':False, 'score':score_,'resultat':results }
            return JsonResponse({'html': render_to_string('correction.html',context,request=request)})
        
@login_required(login_url='connex:log')
def resultatQuiz(request):
    test= Resultats.objects.filter(user=request.user).exists()
    if test == True:
        valide = 0
        echec= 0
        Quizresul=Resultats.objects.filter(user=request.user)
        for testS in Quizresul:
            print(testS.score)
            if testS.score >= testS.quiz.score:
                valide = valide + 1
            else:
                echec =echec + 1
        progression= (valide*100)/(valide+echec)
        progression=int(progression)
        return render(request,"resultats.html",{'Quizresul':Quizresul,'valider':valide,'echec':echec,'progre':progression}) 
    else:
        adherant=Adherant.objects.get(user=request.user)
        check=Souscription.objects.filter(adherant_souscrit=adherant).exists()
        if check == False:
            messages.error(request,'Veuillez vous Abonnez!')
            return redirect('connex:plan')           
        else:
            messages.error(request,'Oups! aucune partie Quiz enregistré')
            return render(request,"noresult.html")

@login_required(login_url='connex:log')
def SupQuiz(request,int_quiz):
    test=Resultats.objects.filter(pk=int_quiz).exists()
    if test == True:
        test=Resultats.objects.get(pk=int_quiz)
        if test.user == request.user or request.user.is_superuser:
            test.delete()
            messages.success(request,'supprimé')
            return redirect('programme:quizresulte')
        else:
            messages.error(request,'pas suprimé')
            return redirect('programme:quizresulte')
    else:
        return redirect('programme:quizresulte')

def deletajax(request,int_quiz):
    test=Resultats.objects.filter(pk=int_quiz).exists()
    if test == True:
        test=Resultats.objects.get(pk=int_quiz)
        if test.user == request.user or request.user.is_superuser:
            test.delete()
            messages.success(request,'supprimé')
            return JsonResponse({'sup':'supprimé'})
            # return redirect('programme:quizresulte')
        else:
            messages.error(request,'pas suprimé')
            return JsonResponse({'sup':'nosupprimé'})
            # return redirect('programme:quizresulte')
    else:
        return redirect('programme:quizresulte')

def favoris(request,int_matiere):
    matiere=Matiere.objects.get(pk=int_matiere)
    if matiere.favoris.filter(id=request.user.id).exists():
        matiere.favoris.remove(request.user)
        messages.error(request,'Favoris supprimé')
    else:
        matiere.favoris.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def favorislecondel(request,int_lecon):
    lecon=Lecons.objects.get(pk=int_lecon)
    if lecon.Favoris.filter(id=request.user.id).exists():
        lecon.Favoris.remove(request.user)
        messages.error(request,'Favoris supprimé')
    else:
        lecon.Favoris.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favoris2(request,int_matiere,int_niveau):
    matiere=Matiere.objects.get(pk=int_matiere)
    if matiere.favoris.filter(id=request.user.id).exists():
        matiere.favoris.remove(request.user)
        fav='supprime'
    else:
        matiere.favoris.add(request.user)
        fav='ajoute'
    return JsonResponse({'check':fav}) 

def favorislecon(request):
    data=request.GET.get('lecon')
    int_lecon=int(data)
    lecon=Lecons.objects.get(pk=int_lecon)
    if lecon.Favoris.filter(id=request.user.id).exists():
        lecon.Favoris.remove(request.user)
        fav='supprime'
    else:
        lecon.Favoris.add(request.user)
        fav='ajoute'
    return JsonResponse({'work':fav})

def favorilist(request):
    favoris=Matiere.objects.filter(favoris=request.user)
    favorislecon=Lecons.objects.filter(Favoris=request.user)
    favlecon=bool
    favmatiere=bool
    if Matiere.objects.filter(favoris=request.user).exists():
        favmatiere=True
        favmatiere=str(favmatiere)
    else:
        favmatiere=False
        favmatiere=str(favmatiere)
    if Lecons.objects.filter(Favoris=request.user).exists():
        favlecon=True
        favlecon=str(favlecon) 
    else:
        favlecon=False 
        favlecon=str(favlecon)      
    return render(request,'favoris.html',{'favoris':favoris,'favorislecon':favorislecon,'favmatiere':favmatiere,'favlecon':favlecon})

@login_required(login_url='connex:log')
def Resultcorrection(request,int_quiz):
    quiz=Quiz.objects.get(pk=int_quiz)
    context={
        'quiz':quiz,
    }
    return render(request,'resulcorrection.html',context)

##############################################

####################General##################   

@login_required(login_url='connex:log')
def genarlquiz(request,int_niveau):
    niveau=Niveau.objects.get(pk=int_niveau)
    quizliste=niveau.Quizniveau.all()
    nombre=GeneralResultats.objects.filter(user=request.user).count()
    nombre=int(nombre)
    fav=bool
    if quizliste :
        fav=True
        fav=str(fav)
    else:
        fav=False
        fav=str(fav)
    context={
        'niveau':niveau,
        'quizs':quizliste,
        'fav':fav,
        'nombre':nombre
    }
    return render(request,'Genralquiz.html',context)

@login_required(login_url='connex:log')
def generalquestion(request,int_niveau,int_quiz):    
    quiz=Generalquiz.objects.get(pk=int_quiz)
    score= None
    jouer = quiz.generalQuiz.filter(user=request.user).exists()
    if jouer == True:
        score = quiz.generalQuiz.filter(user=request.user).first()
        score= int(score.score)
    context={
        'quiz':quiz,
        'jouer':jouer,
        'score':score
    }
    return render(request,'Generalquestion.html',context)

@login_required(login_url='connex:log')
def datatime(request,int_niveau,int_quiz):
    quiz=Generalquiz.objects.get(pk=int_quiz)
    return JsonResponse({'time':quiz.temps})

@login_required(login_url='connex:log')
def generalcorrection(request,int_quiz):
    if request.method == 'POST':
        data=request.POST      
        data_=dict(data)        
        data_.pop('csrfmiddlewaretoken')
        questions=[]
        for  k in data_.keys():
            question=GeneralQuestion.objects.get(text=k)
            questions.append(question)
        user= request.user 
        quiz= Generalquiz.objects.get(pk=int_quiz)
        scrore =0
        mutiplier = 100/ quiz.nombreDequestion
        results=[] 
        correctreponse= None
        for q in questions: 
            reponse_selectionner= request.POST.get(q.text)
            if reponse_selectionner !="":
                questionAns= GeneralReponses.objects.filter(question=q)
                for reponse in questionAns:
                    if reponse_selectionner ==  reponse.text:
                        if reponse.correct:
                            scrore +=1
                            correctreponse = reponse.text
                    else:
                        if reponse.correct:
                            correctreponse = reponse.text
                results.append({str(q): {'reponse_correct':correctreponse, 'reponseselect':reponse_selectionner}  }) 
            else:
                results.append({str(q): 'pas de reponse'}) 

        check1=Adherant.objects.get(user=request.user)
        check2=Souscription.objects.filter(adherant_souscrit=check1).exists()
        if check2== False:
            messages.error(request,'Veuillez vous Abonnez pour voir la correction')
            return redirect('connex:plan')
        score_= scrore * mutiplier
        GeneralResultats.objects.create(quiz=quiz,user=user,score=score_)
        results_={}
        for re in results:
            results_.update(re) 
        if score_>= quiz.score:
            context={'test':True, 'score':score_,'resultat':results_,'quiz':quiz }
            return render(request,'GeneralCorrection.html',context)            
        else: 
            context={'test':False, 'score':score_,'resultat':results_,'quiz':quiz }
            return render(request,'GeneralCorrection.html',context)

@login_required(login_url='connex:log')
def generalResult(request):
    test= GeneralResultats.objects.filter(user=request.user).exists()
    if test == True:
        valide = 0
        echec= 0
        bepc='BEPC'
        Quizresul=GeneralResultats.objects.filter(user=request.user)
      
        for testS in Quizresul:
            voir=testS.quiz.niveauQuiz
            print("sssssssssssss",voir) 
            if testS.score >= testS.quiz.score:
                valide = valide + 1
            else:
                echec =echec + 1        
        progression= (valide*100)/(valide+echec)
        progression=int(progression)
        return render(request,"Generalresultats.html",{'Quizresul':Quizresul,'valider':valide,'echec':echec,'progre':progression}) 
    else:
        adherant=Adherant.objects.get(user=request.user)
        check=Souscription.objects.filter(adherant_souscrit=adherant).exists()
        if check == False:
            messages.error(request,'Veuillez vous Abonnez!')
            return redirect('connex:plan')           
        else:
            messages.error(request,'Oups! aucune partie Quiz enregistré')
            return render(request,"noresult.html")

def generalSupQuiz(request,int_quiz):
    test=GeneralResultats.objects.filter(pk=int_quiz).exists()
    if test == True:
        test=GeneralResultats.objects.get(pk=int_quiz)
        if test.user == request.user or request.user.is_superuser:
            test.delete()
            messages.success(request,'supprimé')
            return redirect('programme:generalresultats')
        else:
            messages.error(request,'pas suprimé')
            return redirect('programme:generalresultats')
    else:
        return redirect('programme:generalresultats')

@login_required(login_url='connex:log')
def generalresultcorrection(request,int_quiz):
    quiz=Generalquiz.objects.get(pk=int_quiz)
    context={
        'quiz':quiz,
    }
    return render(request,'generalresulcorrection.html',context)


#########################################################################

@login_required(login_url='connex:log')
def statistique(request):
    return render(request,'stat.html')


def search(request):
    quizs=Quizjour.objects.all()
    for quiz in quizs:
        print("wwwwwwwwwwwww",quiz.date.strftime('%Y-%m-%d'))
        if str(aujourdhui) == str(quiz.date.strftime('%Y-%m-%d')):
           jouer=Resultasjour.objects.filter(user=request.user).filter(quiz=quiz).exists()
           jouer=str(jouer)  
           return JsonResponse({'status':'disponible','jouer':jouer})
        else:
            return JsonResponse({'status':'indisponible'})
            
@login_required(login_url='connex:log')
def notifacations(request):
    return render(request,"notifiactions.html")

def searchlecon(request,int_matiere):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        series= request.POST.get("series")
        matiere=Matiere.objects.get(pk=int_matiere)
        res = None
        lecons=matiere.lecon.filter(Nom_lecon__icontains=series) 
        if len(lecons)> 0 and len(series)>0 :
            data=[] 
            for lecon in lecons:
                if lecon.lecon_pdf:
                    etats='Disponible'
                    couleur='text-success'
                else:
                    etats='Indisponible'
                    couleur='text-danger'
                item={
                    'id':lecon.pk,
                    'nom':lecon.Nom_lecon,
                    'etats': etats,
                    'couleur':couleur,
                }
                data.append(item)
            res=data
        else:
            res="Aucun résultat trouvé"           
        return JsonResponse({'resulta':res})  
    return JsonResponse({'work':'dcs'})

