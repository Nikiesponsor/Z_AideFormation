from email import message
from django.contrib import messages
import imp
from django.shortcuts import redirect, render
from django.template import context
from .models import Commentaire, Informations
from .forms import Comform
from django.http import Http404, HttpResponse, request, response
from django.conf import settings
import  os

# Create your views here.

def info(request):
    info=Informations.objects.all()
    context={
        "infos":info,
    }
    return render(request,'info.html',context)

def commentaire(request,int_inf):
    info=Informations.objects.get(pk=int_inf)
    listcom=info.info.all()
    form = Comform()
    if request.method == 'POST':
        form = Comform(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.user=request.user
            comment.info=info
            comment.save()
        else:
            messages.error(request,'commentaire non valide')
            return render(request,'commentaire.html',{'form':form})
    context={
        'info':info,
        'listcom':listcom,
        'form':form,
    }
    return render(request,'commentaire.html',context)


def deletcom(request,int_com):
    check=Commentaire.objects.filter(pk=int_com).exists()
    if check == True:
        comm=Commentaire.objects.get(pk=int_com)
        int_inf=comm.info.pk
        if comm.user == request.user or request.user.is_superuser:
            comm.delete()
            messages.success(request,'commentaire supprimé')
            return redirect('comment:comment',int_inf)
        else:
            return redirect('comment:comment',int_inf)
    else:
        return redirect('comment:info')
        

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response=HttpResponse(fh.read(),content_type="application/PDFINFO")
            response['content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404
        
        





    







