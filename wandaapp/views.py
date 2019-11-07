from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from wandaapp.models import Transaction
from django.http import JsonResponse
import img2pdf
from google.cloud import storage
from wandaapp.scripts.OCR_image import async_detect_document, process_result
from wandaapp.scripts.generate_data import generate_data
import pandas as pd
from django.db.models.functions import Cast, TruncDate
from django.db.models import DateTimeField, CharField

def descriptive(request):

    df = pd.DataFrame(list(Transaction.objects.all().values()))
    #df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['date'] = df['date'].astype('str')
    print(df)
    print(df.dtypes)
    tourist_qty = df.groupby(['date', 'type_of_traveler']).aggregate({'user_id': 'count'}).reset_index()
    print(tourist_qty)
    print(tourist_qty.dtypes)
    tourist_qty = tourist_qty.pivot(index='date', columns='type_of_traveler', values='user_id').reset_index()
    tourist_qty = tourist_qty.fillna(0)
    print(tourist_qty)
    tourist_qty = tourist_qty.to_dict()
    print(tourist_qty)
    tourist_qty['date'] = list(tourist_qty['date'].values())
    tourist_qty['Internacional'] = list(tourist_qty['Internacional'].values())
    tourist_qty['Nacional'] = list(tourist_qty['Nacional'].values())
    print(tourist_qty)

    context = {'tourist_qty':tourist_qty}
    return render(request, 'wandaapp/dashboard-finance.html', context)


def sales(request):

    context = {}
    return render(request, 'wandaapp/dashboard-sales.html', context)


@csrf_exempt
def transaction_model(request):

    if request.method == 'POST':

        form = json.loads(request.body)
        tran = Transaction(**form)
        tran.save()

        return JsonResponse({"success":True})
    elif request.method == 'GET':

        trans = list(Transaction.objects.values())
        return JsonResponse({"transactions":trans})

@csrf_exempt
def form(request):
    context = {}

    return render(request, 'wandaapp/form.html', context)


def camera(request):
    context = {}
    return render(request, 'wandaapp/camera.html', context)


@csrf_exempt
def new_image(request):

    print("entro")
    pdf_name = 'pdf_test.pdf'

    pdf_bytes = img2pdf.convert(request.FILES['myfile'])
    file = open(pdf_name, "wb")

    # writing pdf files with chunks
    file.write(pdf_bytes)
    file.close()

    print("escribio pdf")

    storage_client = storage.Client()
    bucket = storage_client.get_bucket('wanda_vision_images')
    blob = bucket.blob(pdf_name)
    blob.upload_from_filename(pdf_name)

    print("Subio a storage")
    try:
        result = process_result(async_detect_document('gs://wanda_vision_images/{}'.format(pdf_name), 'gs://wanda_vision_images/ignore_'))

        tran = Transaction(**result)
        tran.save()

        return JsonResponse({"success": True, "results":result})
    except Exception as e:
        print(str(e))
        return JsonResponse({"success": False})


def populate_db(request):
    generate_data(request, 24)

    return JsonResponse({"success": True})


@csrf_exempt
def crm(request):
    context = {}

    if request.method == 'POST':

        form = dict(request.POST)
        for key, i in form.items():
            form[key] = i[0]
        tran = Transaction(**form)
        tran.save()

    trans = list(Transaction.objects.all().order_by("-date").values())
    context["trans"] = trans

    return render(request, 'wandaapp/crm.html', context)


def upload(request):
    context = {}
    return render(request, 'wandaapp/upload.html', context)
