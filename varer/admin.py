from django.contrib import admin

from varer.models import *

class RåvareInline(admin.TabularInline):
    model = Råvare
    verbose_name_plural = 'Råvarer'

class KontoAdmin(admin.ModelAdmin):
    list_display = ('navn', 'gruppe', 'innkjopskonto', 'salgskonto', 'count_raavarer')
    list_filter = ('gruppe',)
    inlines = [RåvareInline]

    def count_raavarer(self, obj):
        return str(obj.raavarer.count())
    count_raavarer.short_description = 'Antall råvarer'

class RåvareprisInline(admin.TabularInline):
    model = Råvarepris
    verbose_name_plural = 'Priser'

class RåvareAdmin(admin.ModelAdmin):
    inlines = [RåvareprisInline]
    search_fields = ['kategori', 'navn', 'innkjopskonto__id']
    list_display = ('__str__', 'status', 'mengde', 'enhet', 'antall', 'innkjopskonto')
    list_filter = ('innkjopskonto__gruppe',)

class LeverandørAdmin(admin.ModelAdmin):
    list_display = ('navn', 'kommentar')

class SalgsvareRåvareInline(admin.TabularInline):
    model = Salgsvare.raavarer.through
    extra = 0

class SalgsvarePrisInline(admin.TabularInline):
    model = SalgsvarePris
    extra = 0

class SalgsvareAdmin(admin.ModelAdmin):
    inlines = [SalgsvareRåvareInline, SalgsvarePrisInline]
    search_fields = ['kategori', 'navn', 'salgskonto__salgskonto']
    list_display = ('__str__', 'salgskonto')
    list_filter = ('salgskonto__gruppe',)

class SalgskalkyleVareInline(admin.TabularInline):
    model = Salgskalkyle.varer.through

class SalgskalkyleAdmin(admin.ModelAdmin):
    inlines = [SalgskalkyleVareInline]
    search_fields = ['navn']
    list_display = ('navn', 'dato')

class VaretellingAdmin(admin.ModelAdmin):
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
admin.site.register(VaretellingVare)
