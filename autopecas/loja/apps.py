from django.apps import AppConfig

class LojaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loja'
    
    def ready(self):
        pass
        #import loja.signals  # Para futuros sinais