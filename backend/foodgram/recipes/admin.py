from django.contrib import admin
from recipes.models import Content, Ingredient, Recipe, RecipeTag, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorite_amount')
    list_filter = ('tags',)
    search_fields = ('name', 'author__first_name', 'tags__name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')


admin.site.register(Content, ContentAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag)
admin.site.register(Tag)
