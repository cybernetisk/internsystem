from django.contrib import admin
from intern.models import Intern, InternGroup, InternRole, AccessLevel


class InternAdmin(admin.ModelAdmin):
    list_display = ('user', 'active')
    list_filter = ['semester']


class InternRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class InternGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'description')

# Register your models here.
admin.site.register(Intern, InternAdmin)
admin.site.register(InternRole, InternRoleAdmin)
admin.site.register(InternGroup, InternGroupAdmin)
admin.site.register(AccessLevel)
