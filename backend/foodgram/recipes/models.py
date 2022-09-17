from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Класс для ингредиентов"""

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Единицы измерения'
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Класс для тэгов"""

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Имя тега'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=200,
        null=True
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс для рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        null=False,
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=False,
        default=None
    )
    text = models.TextField(
        null=False,
        verbose_name='Изображение'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Content',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время готовки'
    )

    @property
    def favorite_amount(self):
        return self.favorite_recipes.count()
    favorite_amount.fget.short_description = 'В избранном'

    def __str__(self):
        return self.name


class Content(models.Model):
    """Класс для компонентов рецепта"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_to_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='content'
    )
    amount = models.IntegerField(
        null=False,
    )


class RecipeTag(models.Model):
    """Класс для тэгов рецептов"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_to_tag'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_to_recipe'
    )
