from django.db import models


# Create your models here.

class Osayhing(models.Model):
    nimi = models.CharField(max_length=100, unique=True)
    registrikood = models.CharField(max_length=7, unique=True)
    asutamiskuup = models.DateField(auto_now=True)
    kogukapital = models.IntegerField()


class Isik(models.Model):
    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)
    isikukood = models.CharField(max_length=11)
    osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey(Osayhing, on_delete=models.CASCADE)


class JurIsik(models.Model):
    nimi = models.CharField(max_length=100)
    kood = models.CharField(max_length=7)
    osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey(Osayhing, on_delete=models.CASCADE)
