from django.urls import path

from . import views

urlpatterns = [
    path('descriptive', views.descriptive, name='descriptive'),
    path('form', views.form, name='form'),
    path('crm', views.crm, name='crm'),
    path('upload', views.upload, name='upload'),
    path('camera', views.camera, name='camera'),
    path('new-image', views.new_image, name='new-image'),
    path('api/new_transaction', views.transaction_model, name='new_transaction'),
    path('api/populate_db', views.populate_db, name='populate_db'),
]