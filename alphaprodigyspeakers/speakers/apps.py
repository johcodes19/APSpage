from django.apps import AppConfig


class SpeakersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'speakers'

    def ready(self):
        import speakers.signals



    
