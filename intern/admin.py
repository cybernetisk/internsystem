from django.contrib import admin
from intern.models import Intern, InternGroup, Role, AccessLevel, InternRole


class InternAdmin(admin.ModelAdmin):
    list_display = ('user', 'active')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class InternGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'description')

# Register your models here.
admin.site.register(Intern, InternAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InternGroup, InternGroupAdmin)
admin.site.register(AccessLevel)
admin.site.register(InternRole)
