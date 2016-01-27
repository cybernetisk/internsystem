from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from core.models import User, Semester, Card

from django.utils.translation import ugettext_lazy as _

class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('realname', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'realname', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('username', 'realname', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Semester)
admin.site.register(Card)
