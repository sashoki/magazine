# -*- coding: utf-8 -*-

from django.forms import ModelForm
from models import Comments, Brands, Keywords

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        fields = ['comments_text']

class BrandsForm(ModelForm):
    class Meta:
        model = Brands
        fields = ['name']

class KeywordsForm(ModelForm):
    class Meta:
        model = Keywords
        fields = ['name']