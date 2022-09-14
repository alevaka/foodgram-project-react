from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'email')


admin.site.register(User, UserAdmin)
