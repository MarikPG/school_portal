from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('<int:id>/', views.announcement_detail, name='announcement_detail'),
]