from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('survey/', include('surveyapp.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events_and_calendar.urls')),
]
