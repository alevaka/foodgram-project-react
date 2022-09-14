import base64

from django.core.files.base import ContentFile
from recipes.models import Content, Ingredient, Recipe, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    """Декодирование картинки из base64 в файл"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ContentSerializerCreate(serializers.ModelSerializer):
    """Сериализатор содержимого рецепта"""

    id = serializers.IntegerField(source='ingredient_id')

    class Meta:
        model = Content
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    ingredients = IngredientSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True, allow_null=False)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.favorite_recipes.filter(id=user.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.shopping_cart.filter(id=user.id).exists()
        return False

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if repr.get('ingredients') is not None:
            for id in range(len(repr['ingredients'])):
                amount = instance.recipe_to_ingredient.get(
                    ingredient_id=repr['ingredients'][id]['id']).amount
                repr['ingredients'][id]['amount'] = amount

        return repr
