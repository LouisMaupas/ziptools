from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def mail(request):
    template = loader.get_template('mail.html')
    
    data = {
    }
    return HttpResponse(template.render(data))