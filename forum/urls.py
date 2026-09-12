from django.urls import path

from . import views


app_name = "forum"

urlpatterns = [
	path("", views.forum_home, name="index"),
	path("accounts/signup/", views.signup, name="signup"),
	path("threads/", views.thread_list, name="thread_list"),
	path("threads/create/", views.create_thread, name="create_thread"),
	path("threads/<int:thread_id>/", views.thread_detail, name="thread_detail"),
	path("threads/<int:thread_id>/edit/", views.edit_thread, name="edit_thread"),
	path("threads/<int:thread_id>/delete/", views.delete_thread, name="delete_thread"),
	path("posts/<int:post_id>/reaction/<str:reaction>/", views.react_to_post, name="react_to_post"),
]
