from django.apps import AppConfig


class ExercisegamificationConfig(AppConfig):
    name = 'exercisegamification'

    def ready(self):
        import exercisegamification.signals
