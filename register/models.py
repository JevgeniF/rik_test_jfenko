import math
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


class Osayhing(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(unique=True, max_length=100)
    registrikood = models.CharField(unique=True, max_length=7)
    asutamiskuup = models.DateField()
    kogukapital = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.nimi, self.registrikood)

    def clean(self):
        if not self.nimi.replace(' ', '').replace('-', '').isalnum():
            raise ValidationError('Nimi võib sisaldada ainult tähte ja numbrit')
        if not self.registrikood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.asutamiskuup > date.today():
            raise ValidationError('Asutamiskuupäev ei saa olla tulevikus')
        if self.kogukapital is not None and self.kogukapital < 2500:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 2500 EUR')


class Isik(models.Model):
    id = models.BigAutoField(primary_key=True)
    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)
    isikukood = models.CharField(max_length=11)
    f_osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s (%s)' % (self.perenimi, self.eesnimi, self.isikukood)

    def clean(self):
        if not self.eesnimi.replace(' ', '').replace('-', '').isalpha():
            raise ValidationError('Eesnimi võib sisaldada ainult tähte')
        if not self.perenimi.replace(' ', '').replace('-', '').isalpha():
            raise ValidationError('Perenimi võib sisaldada ainult tähte')
        if not self.isikukood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.f_osaniku_osa is not None and self.f_osaniku_osa < 1:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 1 EUR')

        isikukood_sum = 0

        for i in range(9):
            isikukood_sum += int(self.isikukood[i]) * (i + 1)
        isikukood_sum += int(self.isikukood[9]) * 10
        isikukood_div = math.floor(isikukood_sum / 11)
        isikukood_check_num = isikukood_sum - isikukood_div * 11
        if int(self.isikukood[10]) != isikukood_check_num:
            raise ValidationError('Isikukood on vale')


class JurIsik(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(max_length=100)
    kood = models.CharField(max_length=7)
    j_osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' % (self.nimi, self.kood)

    def clean(self):
        if not self.nimi.replace(' ', '').replace('-', '').isalnum():
            raise ValidationError('Nimi võib sisaldada ainult tähte ja numbrit')
        if not self.kood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.j_osaniku_osa is not None and self.j_osaniku_osa < 1:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 1 EUR')
