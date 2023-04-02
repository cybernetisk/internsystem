from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from varer.models import (
    Råvare,
    Råvarepris,
    Salgsvare,
    SalgsvarePris,
    Salgskalkyle,
    Konto,
    Leverandør,
    Varetelling,
    VaretellingVare,
)


class HaveLinkedSalesProductFilter(admin.SimpleListFilter):
    title = _("har lenket salgsprodukt")

    parameter_name = "havelinkedsaleproduct"

    def lookups(self, request, model_admin):
        return (("f", _("Nei")), ("t", _("Ja")))

    def queryset(self, request, queryset):
        if self.value() == "f" or self.value() == "t":
            isnull = True if self.value() == "f" else False
            return queryset.filter(lenket_salgsvare__isnull=isnull)


class RåvareInline(admin.TabularInline):
    model = Råvare
    verbose_name_plural = "Råvarer"


class KontoAdmin(admin.ModelAdmin):
    list_display = ("navn", "gruppe", "innkjopskonto", "salgskonto", "count_raavarer")
    list_filter = ("gruppe",)
    inlines = [RåvareInline]

    def count_raavarer(self, obj):
        return str(obj.raavarer.count())

    count_raavarer.short_description = "Antall råvarer"


class RåvareprisInline(admin.TabularInline):
    model = Råvarepris
    verbose_name_plural = "Priser"


class SalgsvareRåvareInline(admin.TabularInline):
    model = Salgsvare.raavarer.through
    extra = 0


class RåvareAdmin(admin.ModelAdmin):
    inlines = [RåvareprisInline, SalgsvareRåvareInline]
    search_fields = ["kategori", "navn", "innkjopskonto__id"]
    list_display = ("__str__", "status", "mengde", "enhet", "antall", "innkjopskonto")
    list_filter = (
        "innkjopskonto__gruppe",
        "innkjopskonto__navn",
        "status",
        HaveLinkedSalesProductFilter,
    )


class LeverandørAdmin(admin.ModelAdmin):
    list_display = ("navn", "kommentar")


class SalgsvarePrisInline(admin.TabularInline):
    model = SalgsvarePris
    extra = 0


class SalgsvareAdmin(admin.ModelAdmin):
    inlines = [SalgsvareRåvareInline, SalgsvarePrisInline]
    search_fields = ["kategori", "navn", "salgskonto__salgskonto"]
    list_display = ("kassenr", "__str__", "salgskonto", "status")
    list_filter = ("salgskonto__gruppe", "salgskonto__navn", "status", "kategori")


class SalgskalkyleVareInline(admin.TabularInline):
    model = Salgskalkyle.varer.through


class SalgskalkyleAdmin(admin.ModelAdmin):
    inlines = [SalgskalkyleVareInline]
    search_fields = ["navn"]
    list_display = ("navn", "dato")


class VaretellingAdmin(admin.ModelAdmin):
    search_fields = ["tittel", "ansvarlig"]


admin.site.register(Konto, KontoAdmin)
admin.site.register(Råvare, RåvareAdmin)
admin.site.register(Leverandør, LeverandørAdmin)
admin.site.register(Salgsvare, SalgsvareAdmin)
admin.site.register(Salgskalkyle, SalgskalkyleAdmin)
admin.site.register(Varetelling, VaretellingAdmin)
admin.site.register(VaretellingVare)
