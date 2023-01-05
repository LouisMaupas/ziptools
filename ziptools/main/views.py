from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def index(requests):
    template = loader.get_template('index.html')
    global data
    data = {
                "form": "test"
            }
    if requests.GET:
        pass
    elif requests.POST:
        pass
    return HttpResponse(template.render(data))