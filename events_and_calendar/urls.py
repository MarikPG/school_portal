from django.urls import path
from . import views

app_name = 'events_and_calendar'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('calendar/', views.CalendarView.as_view(), name='calendar_view'),
    path('api/events/', views.event_calendar_json, name='calendar_json'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]