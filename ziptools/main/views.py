from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(requests):
    if requests.GET:
        pass
    elif requests.POST:
        pass
    return HttpResponse("Salut")