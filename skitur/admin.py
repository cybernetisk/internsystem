from django.contrib import admin
from skitur.models import Trip, Cabin, Participant, Wish


admin.site.register(Trip)

class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ('trip',)
    list_display = ('trip', 'user', 'phone', 'has_payed', 'has_cancelled')

admin.site.register(Participant, ParticipantAdmin)


class CabinAdmin(admin.ModelAdmin):
    list_filter = ('trip',)
    list_display = ('trip', 'name', 'beds')

admin.site.register(Cabin, CabinAdmin)


class WishAdmin(admin.ModelAdmin):
    list_filter = ('participant__trip',)
    list_display = ('participant', 'wish')


admin.site.register(Wish, WishAdmin)
