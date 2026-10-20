from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("privacy/", TemplateView.as_view(template_name="registration/privacy.html"), name="privacy"),
    path("logout/", views.logout_view, name="logout"),
    path("", include("django.contrib.auth.urls")),
    path("privacy/", TemplateView.as_view(template_name="registration/privacy.html"), name="privacy"),
    path("terms/", TemplateView.as_view(template_name="registration/terms.html"), name="terms"),
]