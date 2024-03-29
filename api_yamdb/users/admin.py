from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role')
    search_fields = ('username',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
