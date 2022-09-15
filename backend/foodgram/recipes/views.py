from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Content, Ingredient, Recipe, RecipeTag, Tag
from recipes.paginatons import CustomPagination
from recipes.permissions import IsAuthorOrAdmin
from recipes.serializers import (ContentSerializerCreate, IngredientSerializer,
                                 RecipeSerializer, TagSerializer)
from rest_framework import permissions, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингридиентов"""

    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset


class TagsViewSet(viewsets.ModelViewSet):
    """Вьюсет для тэгов"""

    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""

    serializer_class = RecipeSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        """Фильтрация рецептов"""

        queryset = Recipe.objects.all().order_by('-id')
        user = self.request.user
        author_id = self.request.query_params.get('author')
        if author_id is not None and author_id.isdigit():
            queryset = queryset.filter(author_id=author_id)
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None:
            if int(is_favorited):
                queryset = queryset.filter(favorite_recipes__id=user.id)
            else:
                queryset = queryset.exclude(favorite_recipes__id=user.id)
        is_in_shopping_cart = self.request.query_params.get(
                                                    'is_in_shopping_cart')
        if is_in_shopping_cart is not None:
            if int(is_in_shopping_cart):
                queryset = queryset.filter(shopping_cart__id=user.id)
            else:
                queryset = queryset.exclude(shopping_cart__id=user.id)
        tag_slug_list = self.request.query_params.getlist('tags')
        if tag_slug_list is not None:
            for tag_slug in tag_slug_list:
                queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def perform_create(self, serializer):
        """Создание нового рецепта"""

        user = self.request.user
        ingredients = serializer.initial_data.pop('ingredients')
        tag_list = []
        if 'tags' in serializer.initial_data:
            tags = serializer.initial_data.pop('tags')
            tag_list = [get_object_or_404(Tag, pk=tag) for tag in tags]
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save(author=user)
        ing_serializer = ContentSerializerCreate(recipe,
                                                 data=ingredients, many=True)
        ing_serializer.is_valid(raise_exception=True)
        contetnt_list = ([Content(recipe=recipe, **item)
                         for item in ing_serializer.validated_data])
        Content.objects.bulk_create(contetnt_list)
        recipe_tag_list = ([RecipeTag(recipe=recipe, tag=item)
                           for item in tag_list])
        RecipeTag.objects.bulk_create(recipe_tag_list)

    def perform_update(self, serializer):
        """Обновление рецепта"""

        ingredients = serializer.initial_data.pop('ingredients')
        tag_list = []
        if 'tags' in serializer.initial_data:
            tags = serializer.initial_data.pop('tags')
            tag_list = [get_object_or_404(Tag, pk=tag) for tag in tags]
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        ing_serializer = ContentSerializerCreate(recipe,
                                                 data=ingredients, many=True)
        ing_serializer.is_valid(raise_exception=True)
        contetnt_list = ([Content(recipe=recipe, **item)
                         for item in ing_serializer.validated_data])
        Content.objects.filter(recipe=recipe).delete()
        Content.objects.bulk_create(contetnt_list)
        RecipeTag.objects.filter(recipe=recipe).delete()
        recipe_tag_list = ([RecipeTag(recipe=recipe, tag=item)
                           for item in tag_list])
        RecipeTag.objects.bulk_create(recipe_tag_list)

    @action(detail=True, methods=['post', 'delete'], name='favorite')
    def favorite(self, request, pk=None):
        """Добавление/удаление в/из избранное"""

        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if recipe.favorite_recipes.filter(id=user.id).exists():
                return Response({'status': 'favorite already exists'},
                                status=views.status.HTTP_400_BAD_REQUEST)
            recipe.favorite_recipes.add(user)
            serializer = RecipeSerializer(recipe, context={'request': request})
            keys = ['id', 'name', 'image', 'cooking_time']
            serializer_data = {key: serializer.data[key] for key in keys}
            return Response(serializer_data)

        if request.method == 'DELETE':
            if recipe.favorite_recipes.filter(id=user.id).exists():
                recipe.favorite_recipes.remove(user)
                return Response({'status': 'favorite deleted'})

            return Response({'status': "favorite doesn't exist"},
                            status=views.status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление в/из корзины"""

        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if recipe.shopping_cart.filter(id=user.id).exists():
                return Response({'status': 'item is already in shopping cart'},
                                status=views.status.HTTP_400_BAD_REQUEST)
            recipe.shopping_cart.add(user)
            serializer = RecipeSerializer(recipe, context={'request': request})
            keys = ['id', 'name', 'image', 'cooking_time']
            serializer_data = {key: serializer.data[key] for key in keys}
            return Response(serializer_data)

        if request.method == 'DELETE':
            if recipe.shopping_cart.filter(id=user.id).exists():
                recipe.shopping_cart.remove(user)
                return Response({'status': 'item deleted from shopping cart'})

            return Response({'status': 'item not in shopping cart'},
                            status=views.status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], name='download_shopping_cart')
    def download_shopping_cart(self, request):
        """Скачивание списка ингридиентов для
           приготовления рецептов из корзины"""

        user = request.user
        if request.method == 'GET':
            shopping_cart_ingredients = user.shopping_cart.values(
                'recipe_to_ingredient__ingredient__name',
                'recipe_to_ingredient__ingredient__measurement_unit'
            ).annotate(amount=Sum('recipe_to_ingredient__amount'))
            text_ingredients = ['Требуемые ингредиенты:\n']
            for ingredient in shopping_cart_ingredients:
                if ingredient[
                 'recipe_to_ingredient__ingredient__name'] is not None:
                    values = list(ingredient.values())
                    text_ingredients.append(
                        f' - {values[0]} ({values[1]}) — {values[2]}\n'
                    )
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = (
                'attachment; filename=shopping_list.txt'
            )
            response.writelines(text_ingredients)
            return response
