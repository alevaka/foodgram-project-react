from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'email')
    search_fields = ('first_name', 'email')


class UserShoppingCart(User.shopping_cart.through):
    class Meta:
        verbose_name_plural = "Списки покупок"
        proxy = True


class UserFavorites(User.favorites.through):
    class Meta:
        verbose_name_plural = "Избранные"
        proxy = True


class UserFavoritesAdmin(admin.ModelAdmin):
    model = User.favorites.through
    list_display = ('pk', 'user', 'recipe')


class UserShoppingCartAdmin(admin.ModelAdmin):
    model = User.shopping_cart.through
    list_display = ('pk', 'user', 'recipe')


admin.site.register(User, UserAdmin)
admin.site.register(UserFavorites, UserFavoritesAdmin)
admin.site.register(UserShoppingCart, UserShoppingCartAdmin)
