# -*- coding: utf-8 -*-

from django.db import models
from varer.models import Salgsvare

class Betalingskonto(models.Model):
    """

    """
    kontonr = models.PositiveSmallIntegerField('Kontonummer', null=False)
    navn = models.CharField('Kontonavn', max_length=100, null=False, blank=False)
    kassenr = models.PositiveSmallIntegerField('Kassenummer', null=False)
    kassenavn = models.CharField('Kassenavn', max_length=15, null=False, blank=False)

class Zrapport(models.Model):
    """
    En Z-rapport. Har et unikt nummer og en tidspunkt
    """
    nummer = models.PositiveIntegerField('Zrapport-nummer', null=False)
    tidspunkt = models.DateTimeField('Tidspunkt', null=False)

class Kvittering(models.Model):
    """
    En kvittering, tilhører en Z-rapport og inneholder flere varetransaksjoner
    """
    zrapport = models.ForeignKey(Zrapport, related_name='kvitteringer', null=False, blank=False)
    nummer = models.PositiveIntegerField('Kvitteringsnummer', null=False)
    tidspunkt = models.DateTimeField('Tidspunkt', null=False)
    #varetransaksjoner = models.ForeignKey('Kassetransaksjon', null=False, blank=False)

class Vareuttak(models.Model):
    """
    Et uttak av varer utenom kassen. Kan være enten til internbruk eller salg.
    """
    tidspunkt = models.DateTimeField('Tidspunkt for uttak', null=False)
    beskrivelse = models.TextField('Beskrivelse av uttak', null=False)
    #varetransaksjoner = models.ForeignKey('Vareuttaktransaksjon', null=False, blank=False)

class Varetransaksjon(models.Model):
    """
    En varetransaksjon er et uttak av et antall av en salgsvare.
    """
    salgsvare = models.ForeignKey(Salgsvare, related_name='transaksjoner', null=False, blank=False)
    antall = models.IntegerField('Antall varer', null=False)
    pris = models.FloatField(help_text='Salgspris inkl. mva')
    tidspunkt = models.DateTimeField('Tidspunkt for transaksjon', null=False)

class Kassetransaksjon(Varetransaksjon):
    """
    En kassetransaksjon er en varetransaksjon med en kobling mot en kvittering
    og derfra videre til en z-rapport.
    """
    kvittering = models.ForeignKey(Kvittering, related_name='transaksjoner', null=False, blank=False)

class Varetuttaktransaksjon(Varetransaksjon):
    """
    En vareuttaktransaksjon er en varetransaksjon knyttet til et vareuttak.
    """
    vareuttak = models.ForeignKey(Vareuttak, related_name='varer', null=False, blank=False)

class Betalingstransaksjon(models.Model):
    betalingskonto = models.ForeignKey(Betalingskonto, related_name='transaksjoner', null=False, blank=False)
    beløp = models.FloatField('Beløp betalt', null=False)
    tidspunkt = models.DateTimeField('Tidspunkt for transaksjon', null=False)

class KasseBetalingstransaksjon(Betalingstransaksjon):
    kvittering = models.ForeignKey(Kvittering, related_name='betalinger', null=False, blank=False)


# Select salgsvare, COUNT(*) varetransaksjon where date >= (SELECT MAX(date) FROM varetelling) GROUP BY salgsvare;

class KassenavnMapping(models.Model):
    nummer = models.PositiveSmallIntegerField('Nummer i kassa', null=False)
    navn = models.CharField('Navn i kassa', max_length=15, null=False)
    salgsvare = models.ForeignKey(Salgsvare, related_name='kassenavn_mappinger', null=False, blank=False)
