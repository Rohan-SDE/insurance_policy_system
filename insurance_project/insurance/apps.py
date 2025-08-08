from django.apps import AppConfig

INSTALLED_APPS = [
    # ...
    'rest_framework',
]


class InsuranceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insurance'
