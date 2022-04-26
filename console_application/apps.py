from django.apps import AppConfig
from django.conf import settings



class ConsoleApplicationConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_application'
    #def ready(self):
    #    if settings.SCHEDULER_DEFAULT:
    #        from price_console import operator
    #        operator.start()
