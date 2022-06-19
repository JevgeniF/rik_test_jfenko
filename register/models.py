import math
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

# A models required for migrations between database and application


# Osaühing model.
class Osayhing(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(unique=True, max_length=100)
    registrikood = models.CharField(unique=True, max_length=7)
    asutamiskuup = models.DateField()
    kogukapital = models.IntegerField()

    def __str__(self):
        """
        It returns a string that contains the name of the company and its registration code
        :return: The name and the registry code of the company.
        """
        return '%s (%s)' % (self.nimi, self.registrikood)

    def clean(self):
        """
        If the name contains anything other than letters and numbers, if the registry code contains anything other than
        numbers, if the establishment date is in the future, or if the total capital is less than 2500, then raise a
        validation error
        """
        if not self.nimi.replace(' ', '').replace('-', '').isalnum():
            raise ValidationError('Nimi võib sisaldada ainult tähte ja numbrit')
        if not self.registrikood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.asutamiskuup > date.today():
            raise ValidationError('Asutamiskuupäev ei saa olla tulevikus')
        if self.kogukapital is not None and self.kogukapital < 2500:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 2500 EUR')


# Isik (Füüsiline isik) model.
class Isik(models.Model):
    id = models.BigAutoField(primary_key=True)
    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)
    isikukood = models.CharField(max_length=11)
    f_osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)

    def __str__(self):
        """
        It returns a string that contains the person's last name, first name, and personal ID code
        :return: The last name, first name and personal ID code of the person.
        """
        return '%s %s (%s)' % (self.perenimi, self.eesnimi, self.isikukood)

    def clean(self):
        """
        It checks if the first name, last name and personal code and person capital are valid
        """
        if not self.eesnimi.replace(' ', '').replace('-', '').isalpha():
            raise ValidationError('Eesnimi võib sisaldada ainult tähte')
        if not self.perenimi.replace(' ', '').replace('-', '').isalpha():
            raise ValidationError('Perenimi võib sisaldada ainult tähte')
        if not self.isikukood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.f_osaniku_osa is not None and self.f_osaniku_osa < 1:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 1 EUR')

        # personal code check number (module 11) control.
        isikukood_sum = 0

        for i in range(9):
            isikukood_sum += int(self.isikukood[i]) * (i + 1)
        isikukood_sum += int(self.isikukood[9]) * 10
        isikukood_check_num = isikukood_sum - math.floor(isikukood_sum / 11) * 11
        if int(self.isikukood[10]) != isikukood_check_num:
            raise ValidationError('Isikukood on vale')


# Juriidiline Isik model.
class JurIsik(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(max_length=100)
    kood = models.CharField(max_length=7)
    j_osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)

    def __str__(self):
        """
        It returns a string representation of the object.
        """
        return '%s (%s)' % (self.nimi, self.kood)

    def clean(self):
        """
        If the name field contains anything other than letters, numbers, spaces, or dashes, raise a validation error.
        If the code field contains anything other than numbers, raise a validation error.
        If the share capital field is not empty and is less than 1, raise a validation error
        """
        if not self.nimi.replace(' ', '').replace('-', '').isalnum():
            raise ValidationError('Nimi võib sisaldada ainult tähte ja numbrit')
        if not self.kood.isnumeric():
            raise ValidationError('Registrikood võib sisaldada ainult numbrit')
        if self.j_osaniku_osa is not None and self.j_osaniku_osa < 1:
            raise ValidationError('Kogukapitali suurus peab olema suurem kui 1 EUR')
