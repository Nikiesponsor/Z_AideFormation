import imp
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from connex.models import User
from django.template.defaultfilters import slugify
# Create your models here.

class Informations(models.Model):
    nomInfo=models.CharField(max_length=200)
    body=RichTextUploadingField(blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)
    pdf=models.FileField(upload_to='PDFINFO')
    link=models.CharField(max_length=500,blank=True,null=True)
    class Meta:
        ordering=['-date']

    def __str__(self):
        return self.nomInfo
    

class Commentaire(models.Model):
    nomCom=models.CharField(max_length=500,blank=True)
    body=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    info=models.ForeignKey(Informations,on_delete=models.CASCADE,related_name='info')
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date']

    def save(self, *args,**kwargs):
        self.nomCom=slugify("commenter par " + str(self.user) + "le" + str(self.date))
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.nomCom


