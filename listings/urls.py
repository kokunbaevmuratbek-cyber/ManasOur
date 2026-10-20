from django.urls import path
from . import views

urlpatterns = [
    path("", views.place_list, name="place_list"),
    path("<int:pk>/", views.place_detail, name="place_detail"),
    path("comments/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]