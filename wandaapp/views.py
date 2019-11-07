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
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from statsmodels.tsa.arima_model import ARIMA

def predictive(request):

    # Clusterization
    df = pd.DataFrame(list(Transaction.objects.all().values('category', 'user_gender', 'companion_type', 'type_of_traveler')))

    le_cat = preprocessing.LabelEncoder()
    le_gender = preprocessing.LabelEncoder()
    le_companion = preprocessing.LabelEncoder()
    le_type = preprocessing.LabelEncoder()

    le_cat.fit(df['category'])
    le_gender.fit(df['user_gender'])
    le_companion.fit(df['companion_type'])
    le_type.fit(df['type_of_traveler'])

    df['category'] = le_cat.transform(df['category'])
    df['user_gender'] = le_gender.transform(df['user_gender'])
    df['companion_type'] = le_companion.transform(df['companion_type'])
    df['type_of_traveler'] = le_type.transform(df['type_of_traveler'])

    kmeans = KMeans(n_clusters=4, random_state=0).fit(df)

    centers = kmeans.cluster_centers_
    centers = [[int(round(c)) for c in cl] for cl in centers]

    for c in range(len(centers)):
        centers[c][0] = le_cat.inverse_transform([centers[c][0]])[0]
        centers[c][1] = le_gender.inverse_transform([centers[c][1]])[0]
        centers[c][2] = le_companion.inverse_transform([centers[c][2]])[0]
        centers[c][3] = le_type.inverse_transform([centers[c][3]])[0]


    # Forecasting

    df = pd.DataFrame(list(Transaction.objects.all().values()))
    tourist_qty = df.groupby('date').aggregate({'user_id': 'count'}).reset_index().sort_values('date')
    tourist_qty = np.asarray(tourist_qty['user_id']).astype('float32')
    model = ARIMA(tourist_qty, order=(1, 1, 0))
    model_fit = model.fit(disp=0)
    prediction = model_fit.predict(start=1, end=100)
    labels = list(range(len(prediction)+len(tourist_qty)))
    context = {'clusters':centers, 'tourism_qty':{'forecast':{'data':list(tourist_qty) + list(prediction), 'labels':labels},
                                                  'old':{'data':list(tourist_qty), 'labels':labels}}}


    return render(request, 'wandaapp/dashboard-predictive.html', context)


def descriptive(request):

    df = pd.DataFrame(list(Transaction.objects.all().values()))
    df['date'] = df['date'].astype('str')

    # Tourists

    tourist_qty = df.groupby(['date', 'type_of_traveler']).aggregate({'user_id': 'count'}).reset_index()
    tourist_qty = tourist_qty.pivot(index='date', columns='type_of_traveler', values='user_id').reset_index()
    tourist_qty = tourist_qty.fillna(0)
    tourist_qty = tourist_qty.to_dict()
    tourist_qty['date'] = list(tourist_qty['date'].values())
    tourist_qty['Internacional'] = list(tourist_qty['Internacional'].values())
    tourist_qty['Nacional'] = list(tourist_qty['Nacional'].values())

    tourist_summary = df.groupby(['type_of_traveler']).aggregate({'user_id': 'count'}).reset_index()
    tourist_summary = tourist_summary.to_dict(orient='records')

    # Products
    products_bar = df.groupby(['type_of_traveler', 'product']).aggregate({'user_id': 'count'}).reset_index()
    products_bar = products_bar.to_dict(orient='records')
    products_bar_dict = {}
    for i in products_bar:
        if i['type_of_traveler'] not in products_bar_dict:
            products_bar_dict[i['type_of_traveler']] = {'label':[], 'data':[]}
        products_bar_dict[i['type_of_traveler']]['label'].append(i['product'])
        products_bar_dict[i['type_of_traveler']]['data'].append(i['user_id'])

    # Category
    category_bar = df.groupby(['type_of_traveler', 'category']).aggregate({'user_id': 'count'}).reset_index()
    category_bar = category_bar.to_dict(orient='records')
    category_bar_dict = {}
    for i in category_bar:
        if i['type_of_traveler'] not in category_bar_dict:
            category_bar_dict[i['type_of_traveler']] = {'label': [], 'data': []}
        category_bar_dict[i['type_of_traveler']]['label'].append(i['category'])
        category_bar_dict[i['type_of_traveler']]['data'].append(i['user_id'])

    # Tipo de acompñante
    companion_type = df.groupby(['companion_type']).aggregate({'user_id': 'count'}).reset_index()
    companion_type = companion_type.rename(columns={'companion_type':'label', 'user_id':'value'})
    companion_type = json.dumps(companion_type.to_dict(orient='records'))
    companion_type = companion_type.replace('"value"','value').replace('"label"', 'label')

    # Average price
    average_price = df.groupby(['date']).aggregate({'price': 'sum'}).reset_index()
    average_price = average_price.to_dict()
    average_price_dict = {}
    average_price_dict['date'] = list(average_price['date'].values())
    average_price_dict['date'] = [ i for i in average_price_dict['date'][:15]]
    average_price_dict['values'] = list(average_price['price'].values())
    average_price_dict['values'] = [i for i in average_price_dict['values'][:15]]
    average_price_dict['average'] = [sum(average_price_dict['values'])/len(average_price_dict['values']) for i in average_price_dict['values']]

    context = {'tourist_qty':tourist_qty, 'tourist_summary':tourist_summary, 'products_bar_dict':products_bar_dict,
               'category_bar_dict':category_bar_dict, 'companion_type':companion_type, 'average_price_dict':average_price_dict}
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
            if key == 'date':
                date = form[key].split('/')
                form[key] = '{}-{}-{}'.format(date[2], date[0], date[1])
        tran = Transaction(**form)
        tran.save()

    df = pd.DataFrame(list(Transaction.objects.all().values()))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    context["trans"] = df.to_dict(orient='records')

    return render(request, 'wandaapp/crm.html', context)


def upload(request):
    context = {}
    return render(request, 'wandaapp/upload.html', context)
