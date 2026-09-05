from django.urls import path

from .views import create_survey, home, survey_complete, take_survey

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_survey, name='create_survey'),
    path('<int:survey_id>/take/', take_survey, name='take_survey'),
    path('complete/', survey_complete, name='survey_complete'),
]
