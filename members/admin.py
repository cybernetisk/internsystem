from django.contrib import admin

from members.models import GeneralAssembly, Member

class GeneralAssemblyAdmin(admin.ModelAdmin):
    list_display = ('semester', 'extraordinary', 'time')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_joined', 'lifetime', 'honorary', 'seller')
    search_fields = ['name']
    list_filter = ('semester', 'lifetime', 'honorary')


# Register your models here.
admin.site.register(GeneralAssembly, GeneralAssemblyAdmin)
admin.site.register(Member, MemberAdmin)
