from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [path('createrecipe',views.CreateRecipe.as_view(),name="createrecipe"),
               path('editrecipe/<int:id>',views.EditRecipe.as_view(),name="editrecipe"),
               path('deleterecipe/<int:id>',views.DeleteRecipe.as_view(),name='deleterecipe'),
               path('viewrecipe/<int:id>/',views.ViewRecipe.as_view(),name="viewrecipe"),
               path('search/', views.search_recipe, name='search_recipes'),
               path('rate_recipe/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),
                path('review_recipe/<int:recipe_id>/', views.review_recipe, name='review_recipe'),


]
