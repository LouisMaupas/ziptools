from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .forms import FormUploadFile
from .utils.handle_upload_file import handle_uploaded_file
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    global data
    data = {}
    if request.method == "GET":
        # form = FormUploadFile()
        # data["form"] = form
        data["message"] = "Nous sommes dans un GET."
    elif request.method == "POST":
        uploaded_file = request.FILES['file-upload']
        # file_name = uploaded_file.name
        # file_type = uploaded_file.content_type
        # form = FormUploadFile(request.POST, request.FILES)
        # handle_uploaded_file(request.FILES['file'])
        # data["form"] = form
        print(uploaded_file.name)
        strg_files_name = []
        for file in uploaded_file:
            strg_files_name.append(file.name)
        data["file_name"] : uploaded_file.name
        data["message"] = "Voici les informations de chaque fichiers :"
        return HttpResponse(template.render(data))
    return HttpResponse(template.render(data))














