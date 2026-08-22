from django.urls import path
from . import views

app_name = 'events_and_calendar'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventListView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventListView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventListView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventListView.as_view(), name='event_delete'),
]