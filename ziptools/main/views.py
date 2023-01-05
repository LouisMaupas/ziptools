from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .forms import FormUploadFile
from .utils.handle_upload_file import handle_uploaded_file
from django.views.decorators.csrf import csrf_exempt
import os
import zipfile
import datetime


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    global data
    data = {}
    if request.method == "GET":
        form = FormUploadFile()
        data["form"] = form
        data["message"] = "Nous sommes dans un GET."
    elif request.method == "POST":
        form = FormUploadFile(request.POST, request.FILES)
        # handle_uploaded_file(request.FILES['file'])
        data["form"] = form
        data["message"] = "Voici les informations de chaque fichiers :"
        messages = []
        files = request.FILES.getlist('file_field')
        for f in files:
            messages.append(f)
    return HttpResponse(template.render(data))
    
# View Page Mail
@csrf_exempt
def mail(request):
    template = loader.get_template('mail.html')
    
    if request.GET:
        pass
    elif request.POST:
        print("POST: " + str(request.POST))
        destinataire = request.POST["destinataire"]
        sujet = request.POST["sujet"]
        corps = request.POST["corps"]
        signature = request.POST["signature"]
        print(destinataire + " " + sujet)
        pass

    signature = ""

    # Récupère le path du fichier zip
    filepath = os.path.join('static', 'tp-kivy.zip')

    # Vérifie que le path désigne bien un fichier zip
    fileCorrect = zipfile.is_zipfile(filepath)
    if fileCorrect:
        # Récupère le fichier zip au path indiqué
        zip = zipfile.ZipFile(filepath)
        # Récupère toutes les infos des fichiers dans le zip
        files = zip.infolist()
        # Parcours tous les fichiers du zip et définit la signature du mail
        signature = "Nom\t\t\t\t\tDernière modification\t\tTaille\n"
        for file in files:
            # Date de la dernière modification du fichier
            filelastmodified = str(datetime.datetime(file.date_time[0], file.date_time[1], file.date_time[2], file.date_time[3], file.date_time[4], file.date_time[5]))
            signature += file.filename + "\t\t\t\t" + filelastmodified + "\t\t" + str(file.file_size) + "\n"

    data = {
        "signature": signature
    }

    return HttpResponse(template.render(data))
