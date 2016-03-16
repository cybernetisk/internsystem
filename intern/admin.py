from django.contrib import admin
from intern.models import Intern, InternGroup, InternRole, AccessLevel

# Register your models here.
admin.site.register(Intern)
admin.site.register(InternRole)
admin.site.register(InternGroup)
admin.site.register(AccessLevel)
