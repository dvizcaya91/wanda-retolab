from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form', views.form, name='form'),
    path('crm', views.crm, name='crm'),
    path('api/new_transaction', views.transaction_model, name='new_transaction'),
]