from django.contrib import admin
from intern.models import (
    Intern,
    InternCard,
    Role,
    AccessLevel,
    InternRole,
    InternLogEntry,
)


class InternAdmin(admin.ModelAdmin):
    list_display = ("user", "active")


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "uio_name", "description")


class InternCardAdmin(admin.ModelAdmin):
    list_display = ("intern", "semester")


class InternRoleAdmin(admin.ModelAdmin):
    list_display = ("intern", "role", "date_added")


class InternLogEntryAdmin(admin.ModelAdmin):
    list_display = ("intern", "changed_by", "time", "description")


# Register your models here.
admin.site.register(Intern, InternAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(AccessLevel, AccessLevelAdmin)
admin.site.register(InternRole)
admin.site.register(InternCard, InternCardAdmin)
admin.site.register(InternLogEntry, InternLogEntryAdmin)
