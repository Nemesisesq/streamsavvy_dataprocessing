from django.apps import AppConfig

from secret_sauce.tasks import listen_to_messenger_for_id


class SecretSauceConfig(AppConfig):
    name = 'secret_sauce'
    verbose_name = "This is to start the show id listener for recomndations"
    def ready(self):
        listen_to_messenger_for_id()
        print("listening for show ids for recomendation")
