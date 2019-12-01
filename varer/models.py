from django.db import models
from core.models import User
from varer.managers import RåvareManager

class Konto(models.Model):
    innkjopskonto = models.PositiveSmallIntegerField()
    varelagerkonto = models.PositiveSmallIntegerField()
    beholdningsendringskonto = models.PositiveSmallIntegerField()
    salgskonto = models.PositiveSmallIntegerField()
    navn = models.CharField(max_length=30)
    gruppe = models.CharField(max_length=20)
    kommentar = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['gruppe', 'innkjopskonto']
        verbose_name_plural = 'kontoer'

    def __str__(self):
        return '%s: %s' % (self.gruppe, self.navn)

class Råvare(models.Model):
    STATUS_CHOICES = (
        ('OK', 'I bruk'),
        ('OLD', 'Utgått')
    )

    kategori = models.CharField(max_length=50, null=True, blank=True)
    navn = models.CharField(max_length=100)
    mengde = models.FloatField()
    enhet = models.CharField(max_length=20)
    mengde_svinn = models.FloatField(default=0)
    antall = models.FloatField(default=1, help_text='Antall salgsbare enheter 1 stk gir')
    innkjopskonto = models.ForeignKey(Konto, related_name='raavarer', on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    lenket_salgsvare = models.ForeignKey('Salgsvare', related_name='lenkede_raavarer', null=True, blank=True, on_delete=models.CASCADE)

    objects = RåvareManager()

    class Meta:
        ordering = ['innkjopskonto__gruppe', 'kategori', 'navn']
        verbose_name_plural = 'råvarer'

    def __str__(self):
        return (self.kategori + ': ' if self.kategori else '') + self.navn

class Leverandør(models.Model):
    navn = models.CharField(max_length=100)
    kommentar = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['navn']
        verbose_name_plural = 'leverandorer'

    def __str__(self):
        return self.navn

class Råvarepris(models.Model):
    TYPE_CHOICES = (
        ('FAKTURA', 'Fakturapris'),
        ('LISTE', 'Listepris'),
        ('UKJENT', 'Ukjent opprinnelse')
    )

    raavare = models.ForeignKey(Råvare, related_name='priser', on_delete=models.CASCADE)
    leverandor = models.ForeignKey(Leverandør, related_name='priser', null=True, blank=True, on_delete=models.CASCADE)
    bestillingskode = models.CharField(max_length=30, null=True, blank=True)
    pris = models.FloatField(help_text="Pris eks mva")
    pant = models.FloatField(help_text="Pant per stk", default=0)
    dato = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='UKJENT')
    aktiv = models.BooleanField(default=True, help_text='Hvorvidt dette er/har vært en reell råvarepris for oss')

    class Meta:
        ordering = ['-dato']
        verbose_name_plural = 'råvarepriser'

    def __str__(self):
        return '%s (%s - %s): kr %g' % (self.raavare, self.dato.isoformat(), self.leverandor, self.pris)

class Salgsvare(models.Model):
    kategori = models.CharField(max_length=50, null=True, blank=True)
    navn = models.CharField(max_length=100)
    salgskonto = models.ForeignKey(Konto, related_name='salgsvarer', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Råvare.STATUS_CHOICES, default='OK')
    kassenr = models.PositiveSmallIntegerField(help_text="Nr i varekatalog i kassa", null=True, blank=True)
    kassenavn = models.CharField(max_length=15, help_text="Navn i varekatalog i kassa", null=True, blank=True)
    raavarer = models.ManyToManyField(Råvare, through='varer.SalgsvareRåvare', related_name='salgsvarer')

    class Meta:
        ordering = ['salgskonto__gruppe', 'kategori', 'navn']
        verbose_name_plural = 'salgsvarer'

    def __str__(self):
        return (self.kategori + ': ' if self.kategori else '') + self.navn

class SalgsvareRåvare(models.Model):
    salgsvare = models.ForeignKey(Salgsvare, on_delete=models.CASCADE)
    raavare = models.ForeignKey(Råvare, on_delete=models.CASCADE)
    mengde = models.FloatField()

    def __str__(self):
        return '%g %s av %s' % (self.mengde, self.raavare.enhet, self.raavare)

class SalgsvarePris(models.Model):
    STATUS_CHOICES = (
        ('FOR', 'Forslag'),
        ('GOD', 'Godkjent forslag'),
        ('KAS', 'Registrert i kasse')
    )

    salgsvare = models.ForeignKey(Salgsvare, related_name='priser', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='FOR')
    dato = models.DateField()
    mva = models.PositiveSmallIntegerField(default='25')
    pris_intern = models.PositiveSmallIntegerField(help_text="Internpris INK mva", null=True, blank=True)
    pris_ekstern = models.PositiveSmallIntegerField(help_text="Eksternpris INK mva", null=True, blank=True)

    class Meta:
        ordering = ['-dato']
        verbose_name_plural = 'salgsvarepriser'

    def __str__(self):
        return '%s (%s - %s) %s / %s' % (self.salgsvare, self.dato.isoformat(), self.status,
                                         ('kr %g' % self.pris_intern) if self.pris_intern != None else 'se ekstern',
                                         ('kr %g' % self.pris_ekstern) if self.pris_ekstern != None else 'ikke salg')

class Salgskalkyle(models.Model):
    navn = models.CharField(max_length=30)
    kommentar = models.TextField(null=True, blank=True)
    dato = models.DateField()
    varer = models.ManyToManyField(Salgsvare, through='varer.SalgskalkyleVare', related_name='salgskalkyler')

    class Meta:
        ordering = ['-dato']
        verbose_name_plural = 'salgskalkyler'

    def __str__(self):
        return '%s (%s)' % (self.navn, self.dato.isoformat())

class SalgskalkyleVare(models.Model):
    kalkyle = models.ForeignKey(Salgskalkyle, on_delete=models.CASCADE)
    salgsvare = models.ForeignKey(Salgsvare, on_delete=models.CASCADE)
    interngrad = models.FloatField(null=True, blank=True, help_text="Prosent andel (antall enheter) solgt til internpris")
    antall = models.PositiveIntegerField()

    class Meta:
        ordering = ['salgsvare']
        verbose_name_plural = 'salgskalkylevarer'

    def __str__(self):
        return '%s (%d stk)' % (self.salgsvare, self.antall)

class Varetelling(models.Model):
    tittel = models.CharField(max_length=50)
    kommentar = models.TextField(null=True, blank=True)
    tid = models.DateTimeField()
    ansvarlig = models.CharField(max_length=100)
    varer = models.ManyToManyField(Råvare, through='varer.VaretellingVare', related_name='varetellinger')
    is_locked = models.BooleanField(default=False, help_text="Sperr tellingen for endringer")

    class Meta:
        ordering = ['-tid']
        verbose_name_plural = 'varetellinger'

    def __str__(self):
        return '%s (%s)' % (self.tittel, str(self.tid.isoformat()))

class VaretellingVare(models.Model):
    varetelling = models.ForeignKey(Varetelling, on_delete=models.CASCADE)
    raavare = models.ForeignKey(Råvare, on_delete=models.CASCADE)
    time_price = models.DateField(null=True, blank=True, help_text="Overstyring av tidspunkt varen skal prises")
    added_by = models.ForeignKey(User, editable=False, null=True, help_text="Brukeren som registrerte oppføringen", on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now_add=True)
    sted = models.CharField(max_length=50, null=True, blank=True)
    antall = models.FloatField()
    antallpant = models.FloatField(help_text="Antall hele forpakninger det skal telles pant for, brukes vanlig antall (avrundet opp) hvis ikke spesifisert", null=True, blank=True)
    kommentar = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['varetelling', '-time_added']

    def __str__(self):
        return '%s (sted: %s) %d stk' % (self.raavare, self.sted, self.antall)
