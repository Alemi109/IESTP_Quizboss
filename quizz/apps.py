from django.apps import AppConfig


class QuizzConfig(AppConfig):
    name = 'quizz'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import quizz.signals
