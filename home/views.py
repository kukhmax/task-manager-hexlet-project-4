from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    context = {
        'hello': _('Hello from Hexlet!'),
        'more': _('More info'),
        'courses': _('Practical programming courses'),
    }
    return render(request, 'home/index.html', context=context)



