from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from wandaapp.models import Transaction
from django.http import JsonResponse


def index(request):

    context = {}
    return render(request, 'wandaapp/dashboard-finance.html', context)


@csrf_exempt
def transaction_model(request):
def form(request):

    if request.method == 'POST':

        form = json.loads(request.body)
        tran = Transaction(**form)
        tran.save()

        return JsonResponse({"success":True})
    elif request.method == 'GET':

        trans = list(Transaction.objects.values())
        return JsonResponse({"transactions":trans})





    context = {}
    return render(request, 'wandaapp/form.html', context)
