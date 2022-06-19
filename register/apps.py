from django.apps import AppConfig


# The RegisterConfig class inherits from AppConfig, and is used to store metadata for the register app.
class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'
