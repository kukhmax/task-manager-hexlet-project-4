from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


def index(request):
    response = render_to_string('home/index.html')
    return HttpResponse(response)
