from django import forms
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'

class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }