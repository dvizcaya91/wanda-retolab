from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    
    context = {}
    return render(request, 'wandaapp/dashboard-finance.html', context)


# Create your views here.
