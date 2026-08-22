from django.urls import path

from . import views


app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('upload/', views.upload_media, name='upload'),
]