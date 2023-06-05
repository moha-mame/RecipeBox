from django.shortcuts import render,redirect
from .forms import CreateRecipeForm
from .models import recipe
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests
from recipes.models import recipe
from django.db import models
from .forms import ReviewForm


# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateRecipe(TemplateView):
    form_class = CreateRecipeForm
    context = {}
    template_name = 'recipes/createrecipe.html'

    def get(self,request,*args,**kwargs):
        user = request.user
        self.context['form'] =self.form_class(initial={'created_by': user})
        return render(request,self.template_name, self.context)

    def post(self,request,*args,**kwargs):
        form = self.form_class(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewprofile')
        else:
            self.context['form'] = form
            return render(request,self.template_name,self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ViewRecipe(TemplateView):
    template_name = 'recipes/viewrecipe.html'
    context ={}

    def get(self,request,*args,**kwargs):
        id =kwargs.get('id')
        obj = get_object_or_404(recipe,pk=id)
        self.context['obj'] = obj
        user = request.user.id
        if user:
            try:
                profile = Profile.objects.get(user=user)
                self.context['profile'] = 'pro_exist'
                return render(request, self.template_name, self.context)
            except Exception:
                return redirect('createprofile')
        return render(request,self.template_name,self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditRecipe(TemplateView):
    form_class =CreateRecipeForm
    context = {}
    template_name = 'recipes/createrecipe.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        recipes = get_object_or_404(recipe, pk=id)
        form = self.form_class(instance=recipes)
        self.context['form'] = form
        return render(request,self.template_name , self.context)

    def post(self,request,*args,**kwargs):
        id = kwargs.get('id')
        recipes = get_object_or_404(recipe, pk=id)
        form = self.form_class(instance=recipes,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewprofile')
        else:
            self.context['form']=form
            return render(request,self.template_name,self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteRecipe(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        recipes = get_object_or_404(recipe, pk=id)
        recipes.delete()
        return redirect('viewprofile')




def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(recipe, pk=recipe_id)
    if request.method == 'POST':
        rating = float(request.POST['rating'])
        recipe.rating = rating
        recipe.save()
        return redirect('viewrecipe', recipe_id=recipe_id)
    else:
        return render(request, 'recipes/viewrecipe.html', {'obj': recipe})


def review_recipe(request, recipe_id):
    recipe = get_object_or_404(recipe, pk=recipe_id)
    if request.method == 'POST':
        review = request.POST['review']
        recipe.review = review
        recipe.save()
        return redirect('viewrecipe', recipe_id=recipe_id)
    else:
        return render(request, 'recipes/viewrecipe.html', {'obj': recipe})



def search_recipes(request):
    query = request.GET.get('query')
    results = recipe.objects.filter(recipe_name__icontains=query)
    context = {
        'search_results': results
    }
    return render(request, 'recipes/search_results.html', context)


'''def search_recipes(request):
    query = request.GET.get('query')
    results = []

    if query:
        # Search by recipe name, ingredient, or category
        results = recipe.objects.filter(
            models.Q(recipe_name__icontains=query) |
            models.Q(ingredient__icontains=query) |
            models.Q(category__icontains=query)
        )

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'recipes/search_results.html', context)
'''
'''
def search_recipes(query):
    api_key = '2a785c168dce4b709d57a406313205de'
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={query}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Process the data and extract the information you need
        recipes = data['results']
        return recipes
    else:
        return None

from .views import search_recipes

def search_view(request):
    query = request.GET.get('query')
    recipes = search_recipes(query)
    return render(request, 'search_results.html', {'recipes': recipes})
    '''