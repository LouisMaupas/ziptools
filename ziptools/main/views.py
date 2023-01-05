from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .utils.sendmail import SendEmail
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
        # Supprime s'il y a déjà un fichier présent
        default_storage.delete(filePath)
        default_storage.save(filePath,file)
        return redirect('/choose')
    return HttpResponse(template.render(data))

@csrf_exempt
def chooseFile(request):
    """ Présente les fichiers qui vont être envoyés puis redirige vers la page d'envoi de mail """
    template = loader.get_template('index.html')
    global data
    data = {
        "page": "choose"
    }
    if request.method == "GET":
        """Affiche les fichiers"""
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
        return redirect('/mail')

    
# View Page Mail
@csrf_exempt
def mail(request):
    template = loader.get_template('mail.html')
    
    signature = ""
    mailSend = -1

    # Récupère le path du fichier zip
    filepath = os.path.join('static', 'ziptools.zip')

    # Vérifie que le path désigne bien un fichier zip
    fileCorrect = zipfile.is_zipfile(filepath)
    if fileCorrect:
        # Récupère le fichier zip au path indiqué
        zip = zipfile.ZipFile(filepath)
        # Récupère toutes les infos des fichiers dans le zip
        files = zip.infolist()
        # Parcours tous les fichiers du zip et définit la signature du mail
        signature = "Nom\t\t\t\tDernière modification\t\tTaille\n"
        for file in files:
            # Date de la dernière modification du fichier
            filelastmodified = str(datetime.datetime(file.date_time[0], file.date_time[1], file.date_time[2], file.date_time[3], file.date_time[4], file.date_time[5]))
            signature += file.filename + "\t\t\t" + filelastmodified + "\t\t" + str(file.file_size) + "\n"


    if request.GET:
        pass
    elif request.POST:
        # Récupération des informations du formulaires en POST
        destinataire = request.POST["destinataire"]
        sujet = request.POST["sujet"]
        corps = request.POST["corps"]
        signatureMail = request.POST["signature"]
        if(destinataire != "" and sujet != ""):
            SendEmail(destinataire, sujet, corps, signatureMail, filepath)
            mailSend = 0

    print(mailSend)
    data = {
        "signature": signature,
        "mailSend": mailSend,
    }
    return HttpResponse(template.render(data))
