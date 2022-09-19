from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'email')
    search_fileds = ('first_name')


class UserFavorites(admin.ModelAdmin):
    model = User
    filter_horizontal = ('favorites',)


admin.site.register(User, UserFavorites)

admin.site.register(User, UserAdmin)
