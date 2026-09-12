from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.list_views, name='list'),
    path('<int:question_id>/', views.detail_views, name='detail'),
    path('<int:question_id>/vote/', views.vote_views, name='vote'),
    path('<int:question_id>/results/', views.results_views, name='results'),
]