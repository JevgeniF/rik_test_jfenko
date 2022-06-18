import os
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rik_test_jfenko.settings')

import django

django.setup()

import random
from register.models import Osayhing, Isik, JurIsik
from faker import Faker

# Faker populated models
faker = Faker()
fakerEe = Faker('et_EE')


# One osayhing population
def populate_osayhing_model():
    fake_nimi = faker.company()
    fake_registrikood = random.randint(1000000, 9999999)
    fake_asutamiskuup = faker.date_between_dates(date(2022, 1, 1), date.today())

    fake_osayhing = Osayhing.objects.get_or_create(
        nimi=fake_nimi,
        registrikood=fake_registrikood,
        asutamiskuup=fake_asutamiskuup,
        kogukapital=2500
    )
    return fake_osayhing[0]


# Osauhingute and osutajate population
def populate_osayhingud_with_oustajad(count=5):
    for i in range(count):
        fake_osayhing = populate_osayhing_model()

        fake_nimi = faker.company()
        fake_kood = random.randint(1000000, 9999999)

        fake_jur_isik = JurIsik.objects.get_or_create(
            nimi=fake_nimi,
            kood=fake_kood,
            osaniku_osa=500,
            asutaja=True,
            osayhing=fake_osayhing
        )

        for j in range(4):
            fake_eesnimi = fakerEe.first_name_est()
            fake_perenimi = fakerEe.last_name_est()
            fake_isikukood = fakerEe.ssn(18, 70)

            fake_isik = Isik.objects.get_or_create(
                eesnimi=fake_eesnimi,
                perenimi=fake_perenimi,
                isikukood=fake_isikukood,
                osaniku_osa=500,
                asutaja=True,
                osayhing=fake_osayhing
            )


if __name__ == '__main__':
    print("Populating data")
    populate_osayhingud_with_oustajad(10)
    print("Populating completed")
