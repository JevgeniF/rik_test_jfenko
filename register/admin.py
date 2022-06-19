from django.contrib import admin

from register.models import Osayhing, Isik, JurIsik

# Registering models with the admin module of Django site.
admin.site.register(Osayhing)
admin.site.register(Isik)
admin.site.register(JurIsik)
