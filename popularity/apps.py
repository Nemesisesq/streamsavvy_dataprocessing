from django.apps import AppConfig

# from popularity.tasks import listen_to_messenger_for_popularity


class PopularityConfig(AppConfig):
    name = 'popularity'
    verbose_name = "This is to start the popularity listener"
    def ready(self):
        pass
        # listen_to_messenger_for_popularity()
        # print("listening for popularity")
#
