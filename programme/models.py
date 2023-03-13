from cgitb import text
import imp
from trace import Trace
from turtle import st
from django.db import models
from django.template.defaultfilters import slugify
from connex.models import  User
from ckeditor_uploader.fields import RichTextUploadingField
from numpy import random
from ckeditor.configs import DEFAULT_CONFIG
from mdeditor.fields import MDTextField
from django_quill.fields import QuillField



class Niveau(models.Model):
    Nom_niveau=models.CharField(max_length=200,null=True,blank=True)
    image_niveau=models.FileField(upload_to='classe',null=True,blank=True)
    slug=models.SlugField(null=True ,blank=True)
    def __str__(self):
        return self.Nom_niveau

    def save(self,*args,**kwargs):
        self.slug=slugify(self.Nom_niveau)
        super().save(*args, **kwargs)

class Matiere(models.Model):
    Nom_matiere=models.CharField(max_length=200,null=True,blank=True)
    image_matiere=models.FileField(upload_to='Matirer',null=True,blank=True) 
    matiere_niveau=models.ForeignKey(Niveau,on_delete=models.CASCADE,related_name='matiere',)
    favoris=models.ManyToManyField(User,related_name='favori',null=True,blank=True)
    slug=models.SlugField(null=True ,blank=True)
    
    def __str__(self):
        return self.Nom_matiere


    def save(self,*args,**kwargs):
        self.slug=slugify(self.Nom_matiere ) 
        super().save(*args, **kwargs)

class Lecons(models.Model):

    Nom_lecon=models.CharField(max_length=100,null=True,blank=True)
    lecon_pdf=models.FileField(upload_to="lecons_pdf",verbose_name="lecon_pdf",null=True,blank=True)
    lecon_niveau=models.ForeignKey(Niveau,on_delete=models.CASCADE,null=True,blank=True)
    lecon_matiere=models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name="lecon",null=True,blank=True)
    numero_lecon=models.PositiveIntegerField(verbose_name='chapitre no',null=True,blank=True)
    slug=models.SlugField(null=True ,blank=True)
    Favoris=models.ManyToManyField(User,related_name='favoris',null=True,blank=True)

    class  Meta:
        ordering= ['numero_lecon']

    def __str__(self):
        return (self.Nom_lecon )

    def save(self,*args,**kwargs):
        self.slug=slugify(self.Nom_lecon)
        super().save(*args, **kwargs)

class Exercices(models.Model):
    Nom_Exercices=models.CharField(max_length=200,null=True,blank=True)
    exercices=models.FileField(upload_to='exercices',verbose_name="exercices",null=True,blank=True)
    exercices_corrige=models.FileField(upload_to='exercices_corrigés',verbose_name="exercices_corrigés",null=True,blank=True)
    exercices_lecons=models.ForeignKey(Lecons,on_delete=models.CASCADE,related_name="exercices",null=True,blank=True)
    exercices_matiere=models.ForeignKey(Matiere,on_delete=models.CASCADE,null=True,blank=True)
    exercices_niveau=models.ForeignKey(Niveau,on_delete=models.CASCADE,null=True,blank=True)
    slug=models.SlugField(null=True ,blank=True)

    def __str__(self):
        return self.Nom_Exercices

    def save(self,*args,**kwargs):
        self.slug=slugify(self.Nom_Exercices )
        super().save(*args, **kwargs)



###############-----QUIZ-----##################
class Quiz(models.Model):
    
    LEVEL=(
        ('Facile','Facile'),
        ('Normal','Normal'),
        ('Difficile','Dificle'),

    )
    disponibilité=(
        ('disponible','disponible'),
        ('indisponible','indisponible')

    )
    nomQuiz=models.CharField(max_length=300)
    numeroQuiz=models.IntegerField(help_text="Questionnaire Numero")
    niveauQuiz=models.ForeignKey(Niveau,on_delete=models.CASCADE)
    matierequiz=models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name="QuizMatiere")
    nombreDequestion=models.IntegerField(help_text="nombre de question")
    temps=models.IntegerField(help_text="temps pour traiter le questionnair")
    score=models.IntegerField(help_text="Point pour le questionnaire")
    dificulte=models.CharField(max_length=200,choices=LEVEL)
    etat=models.CharField(choices=disponibilité,max_length=200,blank=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Quiz numero: {self.numeroQuiz}- Matiere:  {self.matierequiz}"

    def get_question(self):
        questions=list(self.quiz.all())
        random.shuffle(questions)
        return  questions[:self.nombreDequestion]

class QuestionQuiz(models.Model):
    text=models.TextField(null=True,blank=True)
    indication=models.TextField(null=True,blank=True)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="quiz")
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    def get_reponse(self):
        return self.question.all()


class ReponsesQUiz(models.Model):
    # text=RichTextUploadingField(null=True,blank=True,)    
    text= models.TextField(blank=True,null=True)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(QuestionQuiz,on_delete=models.CASCADE,related_name='question')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" question : {self.question.text} , reponse : {self.text} , correcte : {self.correct} "


class Resultats(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='quizmodule')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.FloatField(help_text="score obtenu par l utilisateur")
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class  Meta:
        ordering= ['-date']

    def __str__(self) :
        return  str(self.user)



############################Quiz General######################

class Generalquiz(models.Model):
    LEVEL=(
        ('Facile','Facile'),
        ('Normal','Normal'),
        ('Difficile','Dificle'),

    )
    disponibilité=(
        ('disponible','disponible'),
        ('indisponible','indisponible')

    )
    nomQuiz=models.CharField(max_length=300)
    numeroQuiz=models.IntegerField(help_text="Questionnaire Numero")
    niveauQuiz=models.ForeignKey(Niveau,on_delete=models.CASCADE,related_name="Quizniveau")
    nombreDequestion=models.IntegerField(help_text="nombre de question")
    temps=models.IntegerField(help_text="temps pour traiter le questionnair")
    score=models.IntegerField(help_text="Point pour le questionnaire")
    dificulte=models.CharField(max_length=200,choices=LEVEL)
    date=models.DateTimeField(auto_now_add=True)
    etat=models.CharField(choices=disponibilité,max_length=200,blank=True)

    def get_question(self):
        questions=list(self.Gquiz.all())
        random.shuffle(questions)
        return  questions[:self.nombreDequestion]

    def __str__(self):
        return f" Quiz numero: {self.numeroQuiz}- Niveau:  {self.niveauQuiz}"


class GeneralQuestion(models.Model):
    text=models.TextField(null=True,blank=True)
    indication=models.TextField(null=True,blank=True)
    quiz=models.ForeignKey(Generalquiz,on_delete=models.CASCADE,related_name="Gquiz")
    date=models.DateTimeField(auto_now_add=True)

    def get_reponse(self):
            return self.Gquestion.all()

    def __str__(self):
        return self.text

class GeneralReponses(models.Model):   
    text= models.TextField(blank=True,null=True)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(GeneralQuestion,on_delete=models.CASCADE,related_name='Gquestion')
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" question : {self.question.text} , reponse : {self.text} , correcte : {self.correct}"

class GeneralResultats(models.Model):
    quiz=models.ForeignKey(Generalquiz,on_delete=models.CASCADE,related_name="generalQuiz")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.FloatField(help_text="score obtenu par l utilisateur")
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class  Meta:
        ordering= ['-date']

    def __str__(self) :
        return  str(self.user)



