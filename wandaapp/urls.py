from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form', views.form, name='form'),
    path('camera', views.camera, name='camera'),
    path('new-image', views.new_image, name='new-image'),
    path('api/new_transaction', views.transaction_model, name='new_transaction'),
]