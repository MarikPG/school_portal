from django.urls import path

from . import views


app_name = "gallery"

urlpatterns = [
    path("", views.gallery, name="gallery"),

    path(
        "upload/",
        views.upload_media,
        name="upload"
    ),

    path(
        "edit/<int:pk>/",
        views.edit_media,
        name="edit"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_media,
        name="delete"
    ),
]