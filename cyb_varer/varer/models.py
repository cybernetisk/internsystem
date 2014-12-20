from django.db import models

class Konto(models.Model):
    innkjøpskonto = models.PositiveSmallIntegerField()
    varelagerkonto = models.PositiveSmallIntegerField()
    beholdningsendringskonto = models.PositiveSmallIntegerField()
    salgskonto = models.PositiveSmallIntegerField()
    navn = models.CharField(max_length=30)
    gruppe = models.CharField(max_length=20)
    kommentar = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['gruppe', 'innkjøpskonto']
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
    innkjøpskonto = models.ForeignKey(Konto, related_name='råvarer')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')

    class Meta:
        ordering = ['kategori', 'navn']
        verbose_name_plural = 'råvarer'

    def __str__(self):
        return (self.kategori + ': ' if self.kategori else '') + self.navn

class Leverandør(models.Model):
    navn = models.CharField(max_length=100)
    kommentar = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['navn']
        verbose_name_plural = 'leverandører'

    def __str__(self):
        return self.navn

class Råvarepris(models.Model):
    råvare = models.ForeignKey(Råvare, related_name='priser')
    leverandør = models.ForeignKey(Leverandør, related_name='priser')
    bestillingskode = models.CharField(max_length=30, null=True, blank=True)
    pris = models.FloatField(help_text="Pris eks mva")
    pant = models.FloatField(help_text="Pant per stk", default=0)
    dato = models.DateField()

    class Meta:
        ordering = ['-dato']
        verbose_name_plural = 'råvarepriser'

    def __str__(self):
        return self.råvare.navn + ' (' + self.dato.isoformat() + '): kr ' + str(self.pris)

class Salgsvare(models.Model):
    kategori = models.CharField(max_length=50, null=True, blank=True)
    navn = models.CharField(max_length=100)
    salgskonto = models.ForeignKey(Konto, related_name='salgsvarer')
    status = models.CharField(max_length=10, choices=Råvare.STATUS_CHOICES, default='OK')
    råvarer = models.ManyToManyField(Råvare, through='varer.SalgsvareRåvare', related_name='salgsvarer')

    class Meta:
        ordering = ['kategori', 'navn']
        verbose_name_plural = 'salgsvarer'

    def __str__(self):
        return (self.kategori + ': ' if self.kategori else '') + self.navn

class SalgsvareRåvare(models.Model):
    salgsvare = models.ForeignKey(Salgsvare)
    råvare = models.ForeignKey(Råvare)
    mengde = models.FloatField()

class SalgsvarePris(models.Model):
    STATUS_CHOICES = (
        ('FOR', 'Forslag'),
        ('GOD', 'Godkjent forslag'),
        ('KAS', 'Registrert i kasse')
    )

    salgsvare = models.ForeignKey(Salgsvare)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='FOR')
    dato = models.DateField()
    mva = models.PositiveSmallIntegerField(default='25')
    kassenr = models.PositiveSmallIntegerField(help_text="Nr i varekatalog i kassa", null=True, blank=True)
    pris_intern = models.PositiveSmallIntegerField(help_text="Internpris INK mva", null=True, blank=True)
    pris_ekstern = models.PositiveSmallIntegerField(help_text="Eksternpris INK mva", null=True, blank=True)

    class Meta:
        ordering = ['-dato']
        verbose_name_plural = 'salgsvarepriser'

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
    kalkyle = models.ForeignKey(Salgskalkyle)
    salgsvare = models.ForeignKey(Salgsvare)
    interngrad = models.FloatField(null=True, blank=True, help_text="Prosent andel (antall enheter) solgt til internpris")
    antall = models.PositiveIntegerField()

    class Meta:
        ordering = ['salgsvare']
        verbose_name_plural = 'salgskalkylevarer'

class Varetelling(models.Model):
    tittel = models.CharField(max_length=50)
    kommentar = models.TextField(null=True, blank=True)
    tid = models.DateTimeField()
    ansvarlig = models.CharField(max_length=100)
    varer = models.ManyToManyField(Råvare, through='varer.VaretellingVare', related_name='varetellinger')

    class Meta:
        ordering = ['-tid']
        verbose_name_plural = 'varetellinger'

    def __str__(self):
        return '%s (%s)' % (self.tittel, str(self.tid.isoformat()))

class VaretellingVare(models.Model):
    varetelling = models.ForeignKey(Varetelling)
    råvare = models.ForeignKey(Råvare)
    sted = models.CharField(max_length=50)
    antall = models.FloatField()
    kommentar = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['varetelling', 'råvare']
