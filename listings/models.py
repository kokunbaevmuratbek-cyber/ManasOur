from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
     name = models.CharField(
          max_length=100,
          unique=True
     )

     slug = models.SlugField(
          max_length=100,
          unique=True
     )

     def __str__(self):
          return self.name

class Place(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="listings",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    address = models.CharField(max_length=300, default="")
    popular = models.FloatField()
    review = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f"{self.name}"


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="image"
    )

    image = models.ImageField(
        upload_to="places/",
        default= "default.png"
    )

    is_main = models.BooleanField(
        default=False
    )

    
    def __str__(self):
        return f"{self.place.name} {self.place.address}" 

class Comment(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} → {self.place}"