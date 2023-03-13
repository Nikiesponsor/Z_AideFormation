from lib2to3.pgen2 import token
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import datetime
from datetime import timedelta
from datetime import datetime as dt
aujourdhui = datetime.date.today()


#############################################################

######################---USER-CUSTOM----#######################

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


#### This is User Profile
class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=100, default='',blank=True,null=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    # telphone=PhoneNumberField(null=True,blank=True,)
    ceckbox_info=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.email


#############################################################

######################---Adhesion----#######################

class Historique(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    typelan=models.ForeignKey('PlanAdhesion',on_delete=models.SET_NULL,null=True)
    prix=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    token=models.CharField(max_length=100)
    transaction_id=models.CharField(max_length=100,)
    payer=models.BooleanField(default=False)    
    date =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)

class PlanAdhesion(models.Model):
    FORFAIT= (
        ('FREE','FREE'),
        ('BASIC','BASIC'),
        ('MEDIUM','MEDIUM'),
        ('PRO','PRO'),


    )
    type_adhesion=models.CharField(max_length=200,choices=FORFAIT,default='FREE')
    dure=models.PositiveIntegerField()
    prix=models.DecimalField(default=0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.type_adhesion


class Adherant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='adherant')
    typeplan=models.ForeignKey(PlanAdhesion,on_delete=models.SET_NULL,null=True)
    token=models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return f" {self.user}"


@receiver(post_save, sender=Adherant)
def cretion_souscription(sender, instance, *args, **kwargs):
    if instance:
        check=Souscription.objects.filter(adherant_souscrit=instance).exists()
        if check== True:
            Souscription.objects.filter(adherant_souscrit=instance).update(date_expiration=dt.now().date() + timedelta(days=instance.typeplan.dure))
        else:
            Souscription.objects.create(adherant_souscrit=instance, date_expiration=dt.now().date() + timedelta(days=instance.typeplan.dure) )

class Souscription(models.Model):
    adherant_souscrit=models.ForeignKey(Adherant,on_delete=models.CASCADE,related_name="souscription",null=True, blank=True)
    date_expiration = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True) 
    def __str__(self):
        return f"{self.adherant_souscrit.user}"

@receiver(post_save, sender=Souscription)
def active_update(sender,instance, *args,**kwargs):
    if instance.date_expiration <= aujourdhui:
        soucription= Souscription.objects.get(id=instance.id)
        soucription.delete()
