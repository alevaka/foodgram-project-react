from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorite_recipes'
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='shopping_cart'
    )
    REQUIRED_FIELDS = ["email", "first_name", 'last_name']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
