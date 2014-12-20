from django.contrib import admin

from varer.models import *

class RåvareInline(admin.TabularInline):
    model = Råvare
    verbose_name_plural = 'Råvarer'

class KontoAdmin(admin.ModelAdmin):
    list_display = ('navn', 'gruppe', 'innkjøpskonto', 'salgskonto', 'count_råvarer')
    list_filter = ('gruppe',)
    inlines = [RåvareInline]

    def count_råvarer(self, obj):
        return str(obj.råvarer.count())
    count_råvarer.short_description = 'Antall råvarer'

class RåvareprisInline(admin.TabularInline):
    model = Råvarepris
    verbose_name_plural = 'Priser'

class RåvareAdmin(admin.ModelAdmin):
    inlines = [RåvareprisInline]
    search_fields = ['kategori', 'navn', 'innkjøpskonto']
    list_display = ('__str__', 'innkjøpskonto')
    list_filter = ('innkjøpskonto__gruppe',)

class LeverandørAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'kommentar')

class SalgsvareRåvareInline(admin.TabularInline):
    model = Salgsvare.råvarer.through
    extra = 1
    min_num = 1

class SalgsvareAdmin(admin.ModelAdmin):
    inlines = [SalgsvareRåvareInline]
    search_fields = ['kategori', 'navn', 'salgskonto']

class SalgskalkyleVareInline(admin.TabularInline):
    model = Salgskalkyle.varer.through

class SalgskalkyleAdmin(admin.ModelAdmin):
    inlines = [SalgskalkyleVareInline]
    search_fields = ['navn']

class VaretellingVareInline(admin.TabularInline):
    model = Varetelling.varer.through

class VaretellingAdmin(admin.ModelAdmin):
    inlines = [VaretellingVareInline]
    search_fields = ['tittel', 'ansvarlig']

admin.site.register(Konto, KontoAdmin)
admin.site.register(Råvare, RåvareAdmin)
admin.site.register(Leverandør, LeverandørAdmin)
#admin.site.register(Råvarepris)
admin.site.register(Salgsvare, SalgsvareAdmin)
#admin.site.register(SalgsvareRåvare)
#admin.site.register(SalgsvarePris)
admin.site.register(Salgskalkyle, SalgskalkyleAdmin)
#admin.site.register(SalgskalkyleVare)
admin.site.register(Varetelling, VaretellingAdmin)
#admin.site.register(VaretellingVare)
