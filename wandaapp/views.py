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


def index(request):

    context = {}
    return render(request, 'wandaapp/dashboard-finance.html', context)


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
    result = process_result(async_detect_document('gs://wanda_vision_images/{}'.format(pdf_name), 'gs://wanda_vision_images/ignore_'))

    tran = Transaction(**result)
    tran.save()

    return JsonResponse({"success": True, "results":result})

def populate_db(request):
    generate_data(request, 3)

    return JsonResponse({"success": True})