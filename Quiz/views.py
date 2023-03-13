
from nturl2path import url2pathname
from django.shortcuts import render,redirect
from django.template import context
from .models import *
from django.http import JsonResponse,HttpResponse
from connex.models import *
from programme.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from datetime import datetime as dt
aujourdhui = datetime.date.today()
from django.template.loader import get_template
from xhtml2pdf import pisa,default
from django.http import JsonResponse,HttpResponse,Http404,HttpResponseRedirect
from django.template.defaulttags import register 
from django.shortcuts import render, get_object_or_404
from cinetpay_sdk.s_d_k import Cinetpay

# Create your views here.
@login_required(login_url='connex:log')
def quiz(request):
    quiz=Quizjour.objects.all()
    nombre=Resultasjour.objects.filter(user=request.user).count()
    nombre=int(nombre)
    print("philippppe",nombre)
    context={
        'quizs':quiz,
        'aujourdhui':aujourdhui,
        'nombre':nombre
    }
    return render(request,'quiz.html',context)

@login_required(login_url='connex:log')
def questionquiz(request,int_quiz):
    quiz=Quizjour.objects.get(pk=int_quiz)
    # quiz=get_object_or_404(Quizjour,int_quiz)
    score= None
    jouer = quiz.JourReQuiz.filter(user=request.user).exists()
    if jouer == True:
        score = quiz.JourReQuiz.filter(user=request.user).first()
        score= int(score.score)
    pipo= quiz.get_question()
    adhe=Adherant.objects.get(user=request.user)
    check=Souscription.objects.filter(adherant_souscrit=adhe).exists()
    check=str(check)
    return render(request,'questions.html',{'quiz':quiz,'check':check,'score':score,'jouer':jouer})

def datatimes(request,int_quiz):
    quiz=Quizjour.objects.get(pk=int_quiz)
    return JsonResponse({'time':quiz.temps})

@login_required(login_url='connex:log')
def correctionJour(request,int_quiz):
    if request.method == 'POST':
        data=request.POST      
        data_=dict(data)        
        data_.pop('csrfmiddlewaretoken')
        print(data_)
        questions=[]
        for  k in data_.keys():
            question=Questionsjour.objects.get(text=k)
            questions.append(question)
        user= request.user 
        quiz= Quizjour.objects.get(pk=int_quiz)
        scrore =0
        mutiplier = 100/ quiz.nombreDequestion
        results=[] 
        correctreponse= None
        for q in questions: 
            reponse_selectionner= request.POST.get(q.text)
            if reponse_selectionner !="":
                questionAns= Reponsesjour.objects.filter(question=q)
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
        print("zzzzzzzzzzzzzzzzzzzzzz",results)        
        check1=Adherant.objects.get(user=request.user)
        check2=Souscription.objects.filter(adherant_souscrit=check1).exists()
        check2=str(check2)
        # if check2== False:
        #     messages.error(request,'Veuillez vous Abonnez pour voir la correction')
        #     return redirect('connex:plan')
        score_= scrore * mutiplier
        Resultasjour.objects.create(quiz=quiz,user=user,score=score_)
        results_={}
        for re in results:
            results_.update(re) 
        if score_>= quiz.score:
            context={'test':True, 'score':score_,'resultat':results_,'quiz':quiz,'check2':check2 }
            return render(request,'coorectionjour.html',context)            
        else: 
            context={'test':False, 'score':score_,'resultat':results_,'quiz':quiz,'check2':check2 }
            return render(request,'coorectionjour.html',context)


@login_required(login_url='connex:log')
def resultquizjour(request):

    adherant=Adherant.objects.get(user=request.user)
    check=Souscription.objects.filter(adherant_souscrit=adherant).exists()
    if check == True:
        test= Resultasjour.objects.filter(user=request.user).exists()
        if test == True:
            valide = 0
            echec= 0
            progression=0
            Quizresul=Resultasjour.objects.filter(user=request.user)
            for testS in Quizresul:
                print(testS.score)
                if testS.score >= testS.quiz.score:
                    valide = valide + 1
                else:
                    echec =echec + 1
            progression= (valide*100)/(valide+echec)
            progression=int(progression)
            return render(request,"resultatsjour.html",{'Quizresul':Quizresul,'valider':valide,'echec':echec,'progre':progression}) 
        else:
            messages.error(request,'Oups! aucune partie Quiz enregistré')
            return render(request,"noresult.html")
    else:
        messages.error(request,'Veuillez vous Abonnez!')
        return redirect('connex:plan') 

def favoris(request,int_matiere):
    matiere=Matiere.objects.get(pk=int_matiere)
    if matiere.favoris.filter(id=request.user.id).exists():
        matiere.favoris.remove(request.user)
    else:
        matiere.favoris.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



def supQuizjour(request,int_quiz):
    test=Resultasjour.objects.filter(pk=int_quiz).exists()
    if test == True:
        test=Resultasjour.objects.get(pk=int_quiz)
        if test.user == request.user or request.user.is_superuser:
            test.delete()
            messages.success(request,'supprimé')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
            
            # return redirect('Quiz:resultquizjour')
        else:
            messages.error(request,'pas suprimé')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
            # return redirect('Quiz:resultquizjour')
    else:
        return redirect('Quiz:resultquizjour')

@login_required(login_url='connex:log')
def ResultcorrectionJour(request,int_quiz):
    
    apikey = "125372921762c600b5f24d88.95678537"
    site_id = "125372921762c600b5f24d88.95678537"

    client = Cinetpay(apikey,site_id)

    data = { 
            'amount' : 1000,
            'currency' : "XOF",            
            'transaction_id' : "XXXXXXXXXXXXXXXX",  
            'description' : "TRANSACTION DESCRIPTION",  
            'return_url' : "https://www.exemple.com/return",
            'notify_url' : "https://www.exemple.com/notify", 
            'customer_name' : "XXXXXXXXXXXX",                              
            'customer_surname' : "XXXXXXXXXXXXX",       
        }  
    print(client.PaymentInitialization(data) )
    quiz=Quizjour.objects.get(pk=int_quiz)
    adhe=Adherant.objects.get(user=request.user)
    check=Souscription.objects.filter(adherant_souscrit=adhe).exists()
    check=str(check)
    context={
        'quiz':quiz,
        'check':check,
    }
    return render(request,'resulcorrectionJour.html',context)

def render_pdf_view(request,int_quiz):
    quiz=Quizjour.objects.get(pk=int_quiz)
    print("sssssssssssssssss",default.DEFAULT_CSS)
    template_path = 'pdf.html'
    context = {'quiz': quiz}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Quizpdf.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,default_css="""html {
    font-family: Helvetica;
    font-size: 10px;
    font-weight: normal;
    color: #000000;
    background-color: transparent;
    margin: 0;
    padding: 0;
    line-height: 150%;
    border: 1px none;
    display: grid;
    width: auto;
    height: auto;
    white-space: normal;
}

b,
strong {
    font-weight: bold;
}

i,
em {
    font-style: italic;
}

u {
    text-decoration: underline;
}

s,
strike {
    text-decoration: line-through;
}

a {
    text-decoration: underline;
    color: blue;
}

ins {
    color: green;
    text-decoration: underline;
}
del {
    color: red;
    text-decoration: line-through;
}

pre,
code,
kbd,
samp,
tt {
    font-family: "Courier New";
}

h1,
h2,
h3,
h4,
h5,
h6 {
    font-weight:bold;
    -pdf-outline: true;
    -pdf-outline-open: false;
}

h1 {
    /*18px via YUI Fonts CSS foundation*/
    font-size:138.5%;
    -pdf-outline-level: 0;
}

h2 {
    /*16px via YUI Fonts CSS foundation*/
    font-size:123.1%;
    -pdf-outline-level: 1;
}

h3 {
    /*14px via YUI Fonts CSS foundation*/
    font-size:108%;
    -pdf-outline-level: 2;
}

h4 {
    -pdf-outline-level: 3;
}

h5 {
    -pdf-outline-level: 4;
}

h6 {
    -pdf-outline-level: 5;
}

h1,
h2,
h3,
h4,
h5,
h6,
p,
pre,
hr {
    margin:1em 0;
}

address,
blockquote,
body,
center,
dl,
dir,
div,
fieldset,
form,
h1,
h2,
h3,
h4,
h5,
h6,
hr,
isindex,
menu,
noframes,
noscript,
ol,
p,
pre,
table,
th,
tr,
td,
ul,
li,
dd,
dt,
pdftoc {
    display: block;
}

table {
}

tr,
th,
td {

    vertical-align: middle;
    width: auto;
}

th {
    text-align: center;
    font-weight: bold;
}

center {
    text-align: center;
}

big {
    font-size: 125%;
}

small {
    font-size: 75%;
}


ul {
    margin-left: 1.5em;
    list-style-type: disc;
}

ul ul {
    list-style-type: circle;
}

ul ul ul {
    list-style-type: square;
}

ol {
    list-style-type: decimal;
    margin-left: 1.5em;
}

pre {
    white-space: pre;
}

blockquote {
    margin-left: 1.5em;
    margin-right: 1.5em;
}

noscript {
    display: none;
}

           """)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

