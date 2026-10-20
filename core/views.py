from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from listings.models import Category, Place

from .forms import ContactForm


def home(request):
    places = Place.objects.select_related("category").prefetch_related("image")

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if q:
        places = places.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q)
        )
    if category:
        places = places.filter(Q(category__slug=category) | Q(category__name__iexact=category))

    return render(request, "home.html", {
        "listings": places.order_by("-created_at"),
        "categories": Category.objects.all(),
    })


def contact(request):
    initial = {}
    if request.user.is_authenticated:
        initial = {
            "name": request.user.first_name or request.user.username,
            "email": request.user.email,
        }
    form = ContactForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"{reverse('contact')}?sent=1")
    return render(request, "contact.html", {"form": form, "sent": request.GET.get("sent")})