from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class recipe(models.Model):
    recipe_name = models.CharField(max_length=120)
    ingredient = models.CharField(max_length=600)
    category = models.CharField(max_length=120)
    recipe_pic = models.ImageField(upload_to="images")
    How_to_make = models.CharField(max_length=600)
    created_by = models.ForeignKey(to=User,on_delete=models.CASCADE)


    def __str__(self):
        return self.recipe_name


class Comment(models.Model):
    recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.recipe_name}"
