# Generated by Django 4.0.5 on 2022-06-18 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Osayhing',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nimi', models.CharField(max_length=100, unique=True)),
                ('registrikood', models.CharField(max_length=7, unique=True)),
                ('asutamiskuup', models.DateField()),
                ('kogukapital', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='JurIsik',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nimi', models.CharField(max_length=100)),
                ('kood', models.CharField(max_length=7)),
                ('osaniku_osa', models.IntegerField()),
                ('asutaja', models.BooleanField()),
                ('osayhing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.osayhing')),
            ],
        ),
        migrations.CreateModel(
            name='Isik',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('eesnimi', models.CharField(max_length=100)),
                ('perenimi', models.CharField(max_length=100)),
                ('isikukood', models.CharField(max_length=11)),
                ('osaniku_osa', models.IntegerField()),
                ('asutaja', models.BooleanField()),
                ('osayhing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.osayhing')),
            ],
        ),
    ]
