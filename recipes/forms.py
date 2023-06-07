from django.forms import ModelForm
from .models import recipe
from django import forms
from django.db import models
from .models import Comment

class CreateRecipeForm(ModelForm):
    class Meta:
        model = recipe
        fields = "__all__"
        widgets = {'ingredient':forms.Textarea(),'How_to_make':forms.Textarea(),
                   'created_by':forms.HiddenInput()}
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']          