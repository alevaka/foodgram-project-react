from django.contrib import admin
from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.views import APIUserViewDetail, CustomUserViewSet

router = SimpleRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')

users = DefaultRouter()
users.register("users", CustomUserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/<int:pk>/', APIUserViewDetail.as_view()),
    path('api/', include(users.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(router.urls)),
]
