from django.shortcuts import render,redirect
from .forms import CreateRecipeForm, ReviewForm
from .models import recipe,Review
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from recipes.models import recipe
from django.db import models
from django.http import HttpResponse
from django.views import View
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from weasyprint import HTML, CSS
import tempfile
from django.contrib.staticfiles.storage import FileSystemStorage


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
class ViewRecipe(View):
    template_name = 'recipes/viewrecipe.html'

    def get_context_data(self, request, recipe_id):
        obj = get_object_or_404(recipe, pk=recipe_id)
        reviews = Review.objects.filter(recipe=obj)
        reviews_with_user = []
        for review in reviews:
            user = review.user
            reviews_with_user.append((review, user))
        context = {
            'obj': obj,
            'reviews': reviews_with_user,
        }
        user = request.user.id
        if user:
            try:
                profile = Profile.objects.get(user=user)
                context['profile'] = 'pro_exist'
            except Profile.DoesNotExist:
                return redirect('createprofile')
        return context

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get('id')
        context = self.get_context_data(request, recipe_id)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        recipe_id = kwargs.get('id')
        obj = get_object_or_404(recipe, pk=recipe_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = obj
            review.user = request.user
            review.save()
        context = self.get_context_data(request, recipe_id)
        context['form'] = form
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        if review.user == request.user:
            review.delete()
        return redirect('viewrecipe', id=review.recipe_id)

    def put(self, request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        if review.user == request.user:
            form = ReviewForm(request.PUT, instance=review)
            if form.is_valid():
                form.save()
        return redirect('viewrecipe', id=review.recipe_id)


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


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get('id')
        obj = get_object_or_404(recipe, pk=recipe_id)
        context = {'obj': obj}
        template = get_template('recipes/pdf_template.html')
        html = template.render(context)

        # Generate PDF using WeasyPrint
        pdf_file = tempfile.NamedTemporaryFile(delete=True)
        css_file = tempfile.NamedTemporaryFile(delete=True)

        # Save the CSS for WeasyPrint to access it
        css = "@page { size: A4; margin: 1cm; }"
        with open(css_file.name, 'w') as f:
            f.write(css)

        # Render the HTML template with the CSS and generate the PDF
        HTML(string=html, base_url=FileSystemStorage().base_url).write_pdf(pdf_file.name, stylesheets=[CSS(css_file.name)])

        # Prepare the response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{obj.recipe_name}.pdf"'

        # Set the PDF file content
        with open(pdf_file.name, 'rb') as f:
            response.write(f.read())

        return response
    
def search_recipe(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            recipes = recipe.objects.filter(recipe_name__icontains=query)
            return render(request, 'recipes/search_results.html', {'recipes': recipes})
        else:
            print("No information to show")
            return render(request, 'recipes/search_results.html', {})


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