from django.contrib import admin
from intern.models import Intern, InternCard, InternGroup, Role, AccessLevel, InternRole


class InternAdmin(admin.ModelAdmin):
    list_display = ('user', 'active')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class InternGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'description')

class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uio_name', 'description')

class InternCardAdmin(admin.ModelAdmin):
    list_display = ('intern', 'semester')

class InternRoleAdmin(admin.ModelAdmin):
    list_display = ('intern', 'role', 'date_added')

# Register your models here.
admin.site.register(Intern, InternAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InternGroup, InternGroupAdmin)
admin.site.register(AccessLevel, AccessLevelAdmin)
admin.site.register(InternRole)
admin.site.register(InternCard, InternCardAdmin)
