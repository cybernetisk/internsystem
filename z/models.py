from django.db import models
from varer.models import Salgsvare

# Z-rapport
class Zrapport(models.Model):
    nummer = models.PositiveIntegerField('Zrapport-nummer', null=False)
    tidspunkt = models.DateTimeField('Tidspunkt', null=False)

# En kvittering er en kobling mellom en z-rapport og en
# eller flere transaksjoner i kassen.
class Kvittering(models.Model):
    nummer = models.PositiveIntegerField('Kvitteringsnummer', null=False)
    tidspunkt = models.DateTimeField('Tidspunkt', null=False)
    varetransaksjoner = models.ForeignKey('Kassetransaksjon', null=False, blank=False)


# En varetransaksjon er et uttak av et antall av en salgsvare.
class Varetransaksjon(models.Model):
    salgsvare = models.ForeignKey(Salgsvare, null=False, blank=False)
    antall = models.IntegerField('Antall varer', null=False)

# En kassetransaksjon er en varetransaksjon med en kobling
# mot en kvittering og derfra videre til en z-rapport.
class Kassetransaksjon(Varetransaksjon):
    kvittering = models.ForeignKey(Kvittering, null=False, blank=False)
