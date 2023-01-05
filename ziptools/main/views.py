import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .forms import FormUploadFile
from .utils.handle_upload_file import handle_uploaded_file
from django.views.decorators.csrf import csrf_exempt
import os
import zipfile
import datetime
from django.core.files.storage import default_storage
from django.shortcuts import redirect


@csrf_exempt
def index(request):
    """Page d'accueil permet à l'utilisateur d'upload son fichier zip"""
    template = loader.get_template('index.html')
    global data
    data = {"page": "index"}
    if request.method == "GET":
        """Affiche le formulaire"""
        pass
    elif request.method == "POST":
        """Enregistre le fichier zip et redirige vers la vue qui s'occupera de la 2eme étape """
        # Enregistrement du fichier dans le stockage par défaut
        file = request.FILES['file-upload']
        filePath = '%s/%s' % ('static', 'ziptools.zip')
        default_storage.save(filePath,file)
        return redirect('/choose')
    return HttpResponse(template.render(data))

@csrf_exempt
def chooseFile(request):
    """ Gère la selection des fichiers, enregsitre le nouveau fichier et redirige vers la page d'envoi de mail """
    template = loader.get_template('index.html')
    global data
    data = {
        "page": "choose"
    }
    if request.method == "GET":
        """Affiche la page de selection des fichiers du futur fichier compressé"""
        # Recupère le fichier uploadé
        filepath = os.path.join('static', 'ziptools.zip')
        zip = zipfile.ZipFile(filepath)
        # Le "dezip"
        files = zip.infolist()
        lst_files_to_choose = []
        for f in files:
            lst_files_to_choose.append(f.filename)
        # Envoi les fichiers dezzipés
        data["files"] = lst_files_to_choose
        return HttpResponse(template.render(data))
    elif request.method == "POST":
        """Redirige vers la page d'envoi de mail"""
        # TODO supprime static/ziptools.zip
        return redirect('/mail')

    
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
