
from django.urls  import path
from .import views
from .views import Passwordchange
from django.contrib.auth.decorators import login_required

app_name='connex'

urlpatterns=[
    path('',views.homes,name="home"),
    path('log',views.logine,name="log"),
    path('register',views.register,name="register"),
    path('deconnexion',views.deconnxion,name='deconnexion'),
    path('passwordchange',login_required(Passwordchange.as_view(),login_url='connex:log'),name='password_change'),
    path('profile',views.profile,name='profile'),
    path('profilechange',views.profilechange,name='profilechange'),
    path('plan',views.planAdehsion,name='plan'), 
    path('souscription',views.souscrib,name='souscrib'),
    path('check',views.verification,name='verifaction'),
    path('orienté',views.orientation,name="orientation"),
    path('aabonnement',views.abonnements,name='abonnement'),
    path('aboutus',views.aboutus,name='about'), 
    path('contacts',views.contactus,name='contact'),
    path('profilechange/veri',views.veri,name='veri'),
    path('activation/<uid64>/<token>',views.activate, name='activation'),
    path('activate',views.aftercrate,name='aftercrate'),
    path("usterms",views.conditionsUse,name='Termsuse'),
    path('notification',views.notification,name="notification")
    # path('yoooo',views.set_cookie_consent,name='set_cookie_consent'),
 
]
