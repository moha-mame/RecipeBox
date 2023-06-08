from django.forms import ModelForm
from .models import recipe, Review
from django import forms
from django.db import models


class CreateRecipeForm(ModelForm):
    class Meta:
        model = recipe
        fields = "__all__"
        widgets = {'ingredient':forms.Textarea(),'How_to_make':forms.Textarea(),
                   'created_by':forms.HiddenInput()}
           

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject','review', 'rating']
"""
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) < 10:
            raise ValidationError('Comment must be at least 10 characters long.')
        return comment

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')
        return rating
"""