from django.forms import ModelForm
from .models import recipe
from django import forms

class CreateRecipeForm(ModelForm):
    class Meta:
        model = recipe
        fields = "__all__"
        widgets = {'ingredient':forms.Textarea(),'How_to_make':forms.Textarea(),
                   'created_by':forms.HiddenInput()}
        

class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    review = forms.CharField(widget=forms.Textarea, required=False)