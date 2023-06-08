from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from recipes.views import GeneratePDF
from .views import ViewRecipe

urlpatterns = [path('createrecipe',views.CreateRecipe.as_view(),name="createrecipe"),
               path('editrecipe/<int:id>',views.EditRecipe.as_view(),name="editrecipe"),
               path('deleterecipe/<int:id>',views.DeleteRecipe.as_view(),name='deleterecipe'),
               path('viewrecipe/<int:id>/',views.ViewRecipe.as_view(),name="viewrecipe"),
               path('search/', views.search_recipe, name='search_recipes'),
               path('viewrecipe/<int:id>/download-pdf/', GeneratePDF.as_view(), name='download_pdf'),
               path('recipe/<int:id>/', ViewRecipe.as_view(), name='view_recipe'),

]