from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CommentForm, PlaceForm
from .models import Category, Comment, Place, PlaceImage

MIN_GALLERY = 3
MAX_PHOTOS = 10


@login_required(login_url="login")
def place_add(request):
    form = PlaceForm(request.POST or None)
    photo_error = None

    if request.method == "POST":
        photos = []
        for f in request.FILES.getlist("images")[:MAX_PHOTOS]:
            try:
                photos.append(forms.ImageField().clean(f))
            except ValidationError:
                photo_error = "Один из файлов не является изображением."
                break

        if form.is_valid() and not photo_error:
            place = form.save(commit=False)
            place.owner = request.user
            place.popular = 0
            place.review = 0
            place.save()
            for n, photo in enumerate(photos):
                PlaceImage.objects.create(place=place, image=photo, is_main=(n == 0))
            return redirect("place_detail", pk=place.pk)

    return render(request, "place_add.html", {"form": form, "photo_error": photo_error})


def place_list(request):
    places = Place.objects.select_related("category").prefetch_related("image")
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "")

    if q:
        places = places.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q)
        )
    if category:
        places = places.filter(Q(category__slug=category) | Q(category__name__iexact=category))

    if sort == "popular":
        places = places.order_by("-popular", "-review")
    elif sort == "new":
        places = places.order_by("-created_at")
    else:
        places = places.order_by("name")

    return render(request, "place_list.html", {
        "listings": places,
        "categories": Category.objects.all(),
        "sort": sort,
        "q": q,
        "category": category,
    })



def place_detail(request, pk):
    place = get_object_or_404(
        Place.objects.select_related("category", "owner").prefetch_related("image"),
        pk=pk,
    )

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.path, login_url="login")
        if form.is_valid():
            Comment.objects.create(place=place, author=request.user, text=form.cleaned_data["text"])
            return redirect(f"{request.path}#comments")

    images = sorted(place.image.all(), key=lambda img: not img.is_main)
    placeholders = range(max(0, MIN_GALLERY - len(images)))
    return render(request, "place_detail.html", {
        "place": place,
        "images": images,
        "placeholders": placeholders,
        "total": len(images) + len(placeholders),
        "comments": place.comments.select_related("author"),
        "comment_form": form,
    })


@login_required(login_url="login")
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    place_id = comment.place_id
    if comment.author_id == request.user.id or request.user.is_staff:
        comment.delete()
    return redirect(f"{reverse('place_detail', args=[place_id])}#comments")