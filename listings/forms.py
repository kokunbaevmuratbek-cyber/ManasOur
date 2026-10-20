from django import forms

from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name", "category", "address", "description"]

class CommentForm(forms.Form):
    text = forms.CharField(max_length=1000, strip=True)