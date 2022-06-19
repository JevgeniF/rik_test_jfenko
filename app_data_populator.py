# Faker database population script.
import os
from datetime import date

# Setting the environment variable `DJANGO_SETTINGS_MODULE` to the value `rik_test_jfenko.settings`.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rik_test_jfenko.settings')

import django

# Setting up the Django environment.
django.setup()

import random
from register.models import Osayhing, Isik, JurIsik
from faker import Faker

# Faker
faker = Faker()
# Faker estonian localization
fakerEe = Faker('et_EE')


def populate_osayhing_model():
    """
    It creates a fake company, and returns the company object
    :return: The first element of the tuple is being returned.
    """
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


def populate_osayhingud_with_oustajad(count=5):
    """
    It creates a fake company, then creates a fake juridical person with a random code and a random name, then creates 4
    fake people with random names and random SSN's

    param count: how many times the function should run, defaults to 5 (optional)
    """
    for i in range(count):
        fake_osayhing = populate_osayhing_model()

        fake_nimi = faker.company()
        fake_kood = random.randint(1000000, 9999999)

        JurIsik.objects.get_or_create(
            nimi=fake_nimi,
            kood=fake_kood,
            j_osaniku_osa=500,
            asutaja=True,
            osayhing=fake_osayhing
        )

        for j in range(4):
            fake_eesnimi = fakerEe.first_name_est()
            fake_perenimi = fakerEe.last_name_est()
            fake_isikukood = fakerEe.ssn(18, 70)

            Isik.objects.get_or_create(
                eesnimi=fake_eesnimi,
                perenimi=fake_perenimi,
                isikukood=fake_isikukood,
                f_osaniku_osa=500,
                asutaja=True,
                osayhing=fake_osayhing
            )


# Script starting function.
if __name__ == '__main__':
    print("Populating data")
    populate_osayhingud_with_oustajad(10)
    print("Populating completed")
