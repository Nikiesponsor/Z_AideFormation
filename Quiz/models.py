from django.conf import settings
from django.db import models
from django.http import request
from django.template import base
from django.template.defaultfilters import slugify
from connex.models import  User,Adherant,Souscription
from numpy import random
from django.shortcuts import render,redirect
from ckeditor_uploader.fields import RichTextUploadingField



class Quizjour(models.Model):
    disponibilité=(
        ('disponible','disponible'),
        ('indisponible','indisponible')

    )
    nomQuiz=models.CharField(max_length=300)
    numeroQuiz=models.IntegerField(help_text="Questionnaire Numero")
    nombreDequestion=models.IntegerField(help_text="nombre de question")
    temps=models.IntegerField(help_text="temps pour traiter le questionnair")
    score=models.IntegerField(help_text="Point pour le questionnaire")
    date=models.DateTimeField(auto_now_add=True)
    etat=models.CharField(choices=disponibilité,max_length=200,blank=True)

    def get_question(self):
        questions=list(self.Quizjou.all())
        # random.shuffle(questions)
        return  questions[:self.nombreDequestion]

    class  Meta:
        ordering= ['-date']

    def __str__(self):
        return f" Quiz numero: {self.numeroQuiz}"



class Questionsjour(models.Model):
    # text=RichTextUploadingField(null=True,blank=True,) 
    text=models.TextField(null=True,blank=True)
    indication=models.TextField(null=True,blank=True)
    image=models.FileField(upload_to='imagequestion',blank=True)
    quiz=models.ForeignKey(Quizjour,on_delete=models.CASCADE,related_name="Quizjou")
    date=models.DateTimeField(auto_now_add=True)

    def get_reponse(self):
            return self.questionjou.all()

    def __str__(self):
        return self.text

class Reponsesjour(models.Model):
    text= models.TextField(blank=True,null=True)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Questionsjour,on_delete=models.CASCADE,related_name='questionjou')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" question : {self.question.text} , reponse : {self.text} , correcte : {self.correct}"

class Resultasjour(models.Model):
    quiz=models.ForeignKey(Quizjour,on_delete=models.CASCADE,related_name="JourReQuiz")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.FloatField(help_text="score obtenu par l utilisateur")
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class  Meta:
        ordering= ['-date']

    def __str__(self) :
        return  str(self.user)
