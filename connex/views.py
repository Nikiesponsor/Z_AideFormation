from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import  get_current_site
from .token import genToken
from email import message
import email
from lib2to3.pgen2 import token
from tabnanny import check
from django.shortcuts import redirect, render
from .forms import LoginForm, ReqisterForm, ProfileForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from .forms import ChangepasswordForm
from django.urls.base import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView,PasswordResetConfirmView
from .models import Adherant, Historique, PlanAdhesion, Souscription, User
from django.conf import settings
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
from datetime import datetime as dt
aujourdhui = datetime.date.today()
from django.core.mail import send_mail , EmailMessage
import paydunya
from paydunya import Store
from paydunya import InvoiceItem, Store
from cinetpay_sdk.s_d_k import Cinetpay
import hashlib
import random
import string





##############################################
# payement





###############################################

##################---Acceuil---################

def homes(request):
    checkAdhe=Adherant.objects.filter(user_id=request.user.id).exists()
    if checkAdhe == True:
        adhe=Adherant.objects.get(user=request.user)
        check2=Souscription.objects.filter(adherant_souscrit=adhe).exists()
        if check2 == True:
            sous=Souscription.objects.get(adherant_souscrit=adhe)
            plan=str(sous.adherant_souscrit.typeplan)
            return render(request,'home.html',{'plan':plan}) 
        else:
            plan= str(adhe.typeplan)
            return render(request,'home.html',{'plan':plan})
    else:
       return render(request,'home.html')

###############################################

######################---LOGIN----#############
def logine(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password= form.cleaned_data['password']
            user = authenticate(email=email,password=password)
            # my_user= User.objects.get(email=email)
            print("wwwwwwwwwwwwwwwwwwwwww",user)

            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'Connexion réussie')
                    return redirect('programme:niveau')
                else:
                    messages.error(request,'Veuillez activer votre compte!')
                    return redirect('connex:home')
            # elif my_user.is_active == False and my_user == True:
            #      messages.error(request,'Compte pas activé')
            #      return render(request,'loginZ.html',{'form':form})
            else:
                messages.error(request,'identifiant ou mot de passe incorrect')
                return render(request,'loginZ.html',{'form':form})
        else:
            return render(request,'loginZ.html',{'form':form})
    else:
        form = LoginForm()
        return render(request,'loginZ.html',{'form':form})

###############################################

###############---REGISTER----#################
def register(request):
    if request.method == 'POST':
        form = ReqisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)          
            user.is_active= False
            user.save()
            gratuit=PlanAdhesion.objects.get(type_adhesion='FREE')
            Adherant.objects.create(user=user,typeplan=gratuit)
            #message de bienvenue sur Z_aide
            subjet='Bienvenue sur Z_aide'
            message="Bienvenue " + user.last_name+ " " + user.first_name + " " + "Nous sommes heureux de vous compter parmi nos abonnez \n\n\n Merci pour votre confiance "
            from_email=settings.EMAIL_HOST_USER
            to_user_email=[user.email]
            send_mail(
                subjet,
                message,
                from_email,
                to_user_email,
                fail_silently=False
            )
            #message de validation de compte
            curent_site= get_current_site(request)
            email_subject='Validation de votre compte'
            messagconfirm= render_to_string("confirmationEmail.html",{
                'nom':user.last_name,
                'prenom':user.first_name,
                'domain':curent_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': genToken.make_token(user)
            })
            email = EmailMessage(
               email_subject,
               messagconfirm,
               settings.EMAIL_HOST_USER,
               [user.email]
            )
            email.fail_silently= False 
            email.send()  
            messages.success(request,'Votre compte a été crée avec success ')
            return redirect('connex:aftercrate')                   
        else:           
            return render(request,'register.html',{'form':form})
    else:
        form = ReqisterForm()
        return render(request,'register.html',{'form':form})
def aftercrate(request):
    return render(request,'afterRegister.html')

def activate(request,uid64,token):
    try:
        uid= force_text(urlsafe_base64_decode(uid64))
        user= User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user= None
    if user is not None and genToken.check_token(user,token):
        user.is_active= True
        user.save()
        messages.success(request,'Votre compte a été activé avec succes')
        return redirect('connex:log')
    else:
        messages.error(request,'activation échouée')
        return redirect('connex:home')

#########################################################

######################---LOGOUT----#######################

def deconnxion(request):
    logout(request)
    return redirect('connex:home') 

#############################################################

######################---PASSWORDCHANGE----################## 

      
class Passwordchange(SuccessMessageMixin,PasswordChangeView):
    template_name="password_change_form.html"
    success_url=reverse_lazy('connex:home')
    form_class=ChangepasswordForm
    success_message="Mot de passe changer avec success"
    error_message="verifier les informations"

###################reset password###############

# class Passwordsrest(SuccessMessageMixin,PasswordResetConfirmView):
#     template_name="password_reset_form.html"
#     success_url=reverse_lazy('connex:log')
#     form_class=ResetpasswordForm
#     success_message="mot de passe changer avec success"
#     error_message="verifier les information"


#############################################################

######################---PROfile----################## 

 
@login_required(login_url='connex:log')
def profile(request):
    profile= User.objects.get(email=request.user.email)
    abon=Adherant.objects.get(user=profile)
    check=Souscription.objects.filter(adherant_souscrit=abon).exists()
    if check == True:        
       check=str(abon.typeplan)
       date=Souscription.objects.get(adherant_souscrit=abon)
       return render(request,'profile.html',{'profile':profile,'abon':check,'date':date})
    else:
        check='FREE'       
        return render(request,'profile.html',{'profile':profile,'abon':check,})

@login_required(login_url='connex:log')
def profilechange(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            nom= form.cleaned_data['nom']
            prenom= form.cleaned_data['prenom']
            User.objects.filter(email=request.user.email).update(last_name=nom,first_name=prenom,)
            messages.success(request,'informations modifieés avec success')
            return redirect('connex:home')
        else:
            messages.error(request,'formulaire non valide')
            return render(request,'profilechange.html',{'form':form})
    else:
        form = ProfileForm()
        return render(request,'profilechange.html',{'form':form})

######################################################################
###################---Abonnement et Souscriptions----##################  
@login_required(login_url='connex:log')
def planAdehsion(request):
    plan= Adherant.objects.get(user=request.user)
    check=Souscription.objects.filter(adherant_souscrit=plan).exists()
    if check == True:
        sous=Souscription.objects.get(adherant_souscrit=plan)
        safe=str(sous.adherant_souscrit.typeplan)
        return render(request,'plan.html',{'safe':safe})
    else:
        return render(request,'plan.html')

@login_required(login_url='connex:log')
def souscrib(request):
    plan=request.GET.get('plan')
    checkplan=PlanAdhesion.objects.filter(type_adhesion=plan).exists()
    if checkplan==False:
        messages.error(request,'erreur')
        return redirect('connex:plan') 
    checkplan=PlanAdhesion.objects.get(type_adhesion=plan)
    prix=int(checkplan.prix)
    print(prix)
    apikey = settings.CINETPAY_API_KEY
    site_id = settings.CINETPAY_SITE_ID
    client = Cinetpay(apikey,site_id)
    # Générer une chaîne de 12 caractères aléatoires
    transaction_id= ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    data = { 
        'amount' : prix,
        'currency' : "XOF",            
        'transaction_id' : transaction_id,  
        'description' : "Abonnement a Z_aide", 
        'return_url' : "http://127.0.0.1:8000/check",
        'notify_url' : "http://127.0.0.1:8000/notification",        
        'customer_name' : request.user.last_name,                              
        'customer_surname' : request.user.first_name,       
         }  
    donnee=client.PaymentInitialization(data)
    check1=donnee['code']
    if check1== '201':
        tokens=donnee['data']['payment_token']
        link=donnee["data"]["payment_url"]
        instance=Historique.objects.create(user=request.user,typelan=checkplan,prix=prix,token=tokens,transaction_id=transaction_id)
        Adherant.objects.filter(user=instance.user).update(token=tokens)
        user=Historique.objects.filter(user=request.user).last()
        print("pour veri avec TransactionVerfication_token",client.TransactionVerfication_token("f36b3ebb2cae6a83c733ab17eaf5987b295f9159ff9205c92fa4e3c2fb5138b7059d1494f172817a3e024e71cedcb6e5e45c5ae664b9e8"))
        return HttpResponseRedirect(link)   
    else:
        messages.error(request,"erreur veuillez réessayer ")
        return redirect('connex:plan')
def verification(request):
    apikey = settings.CINETPAY_API_KEY
    site_id = settings.CINETPAY_SITE_ID
    client = Cinetpay(apikey,site_id)
    user=Historique.objects.filter(user=request.usuer).last()
    tokens=user.token
    token =tokens
    print("pour veri avec TransactionVerfication_token",client.TransactionVerfication_token(token))
    return render(request,"verification.html")

def notification(request):
    print("Pour notifiaction post",request.POST)
    return render(request,"notification.html")
    
def orientation(request):
    return render(request,'orientation.html')

def abonnements(request):
    return render(request,'abonnement.html')

def aboutus(request):
    return render(request,'about.html')

def contactus(request):
    if request.method=='POST':
        nom=request.POST.get("name")
        prenom=request.user.first_name
        emails=request.POST.get("email")
        objet=request.POST.get("subject")
        message=request.POST.get("message")

        emails=str(emails)
        html=render_to_string('sendemail.html',{
            'nom':nom,
            'prenom':prenom,
            'email':emails,
            'objet':objet,
            'message':message,
        }
                              
        )
        print(nom,emails,objet,message)
        send_mail(
            objet,
            message,
            emails,
            ['zaideelearning@gmail.com',],
            html_message=html,
            fail_silently=False
        )
        return render(request,'contact.html',{'nom':nom})        
    return render(request,'contact.html',{})

def veri(request):
    pipo=User.objects.get(email=request.user)
    nom=pipo.last_name
    prenom=pipo.first_name
    return JsonResponse({
        'nom':nom,
        'prenom':prenom,
    })

def conditionsUse(request):
    return render(request,'UseTerms.html')


# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect

# @csrf_exempt
# def set_cookie_consent(request):
#     if request.method == 'POST':
#         if request.POST.get('cookie_consent') == 'full':
#             # L'utilisateur a accepté tous les cookies
#             response = HttpResponse("Cookie consent set to 'full'")
#             response.set_cookie('cookie_consent', 'full')
#             return response
#         elif request.POST.get('cookie_consent') == 'necessary':
#             # L'utilisateur a accepté les cookies nécessaires seulement
#             response = HttpResponse("Cookie consent set to 'necessary'")
#             response.set_cookie('cookie_consent', 'necessary')
#             return response
#     # Rediriger l'utilisateur vers la page précédente s'il y a une erreur ou si la méthode HTTP n'est pas "POST"
#     return redirect(request.META.get('HTTP_REFERER', '/'))




