from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from core.views import contact, home
from listings.views import place_add

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("events/", TemplateView.as_view(template_name="events.html"), name="events"),
    path("contact/", contact, name="contact"),
    path("places/add/", place_add, name="place_add"),
    path("places/", include("listings.urls")),
    path("user/", include("registration.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)