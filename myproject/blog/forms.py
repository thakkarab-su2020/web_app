from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Book , BookImage


class BookForm(forms.ModelForm):
    class Meta:
        model= Book
        fields = ['isbn','title', 'authors','publication_date','quantity','price']



class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = BookImage
        fields = ('image', )