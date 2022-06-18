from django.db import models

class Osayhing(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(unique=True, max_length=100)
    registrikood = models.CharField(unique=True, max_length=7)
    asutamiskuup = models.DateField()
    kogukapital = models.IntegerField()

class Isik(models.Model):
    id = models.BigAutoField(primary_key=True)
    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)
    isikukood = models.CharField(max_length=11)
    osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)


class JurIsik(models.Model):
    id = models.BigAutoField(primary_key=True)
    nimi = models.CharField(max_length=100)
    kood = models.CharField(max_length=7)
    osaniku_osa = models.IntegerField()
    asutaja = models.BooleanField()
    osayhing = models.ForeignKey('Osayhing', on_delete=models.CASCADE)
