from django.conf import settings
from django.shortcuts import render, redirect , HttpResponseRedirect
from .forms import FormPreview
from .forms import Imageform
from .models import Certificate
from .models import FormInformation
from .apps import CreateCertificate
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import csv

POST = 10

@login_required(login_url='/login/')
def index(request):
    global POST
    model = FormPreview(request.POST or None)
    cert = Imageform(request.POST or None)
    if request.method == 'POST':
        system = request.POST.get('system')
        if system == 'Preview':
            id = request.POST.get('name')
            if id == None or id == '':
                return redirect('core:index')
            POST = request.POST
            evento = request.POST.get('event')
            data = request.POST.get('date')
            body = request.POST.get('body')
            image = Certificate.objects.get(id=id)
            obj = CreateCertificate()
            obj.PreviewCretificate(str(image.image), data, evento, body)
            return redirect('core:index')
        if system == 'Finalizar':
            try:
                form = FormPreview(POST, request.FILES)
                if os.path.isfile(os.path.join(settings.MEDIA_STATIC, 'certificado.png')):
                    form.save()
                    with open(os.path.join(settings.MEDIA_ROOT,'planilhas' ,str(request.FILES['plan']))) as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=',')
                        for row in spamreader:
                            obj = CreateCertificate()
                            obj.SendEmail(row[0],row[1])
                        obj.remove()
            except:
                return render(request, 'erro.html')

            return redirect('core:upload')

        else:
            return render(request, 'index.html', {
            'cert': cert,
            'model': model,
            })
    else:
            return render(request, 'index.html', {
            'cert': cert,
            'model': model,
            })
   
@login_required(login_url='/login/')        
def support(request):
    return render(request, 'support.html')

@login_required(login_url='/login/')
def upload(request):
    form = FormInformation.objects.all()
    return render(request, 'upload_file.html', {
        'form':form
    })
    
def login_(request):
    return render(request, 'login.html')

@csrf_protect
def login_submit(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')
        else:
            messages.error(request, 'Usuário ou senha inválido. Por favor tentar novamente ou entrar em contato com administrador')
    return redirect('core:login')

    
def logout_(request):
    obj = CreateCertificate()
    obj.remove()
    logout(request)
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    return redirect('core:login')


@login_required(login_url='/login/')        
def contato(request):
    return render(request, 'contato.html')