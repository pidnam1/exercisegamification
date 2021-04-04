from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    name = models.TextField(max_length=500, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_superuser:
            pass
        else:
            instance.profile.save()

    def __str__(self):
        return self.user.username
class Goals(models.Model):
    # ...
    Goal_title = models.CharField(max_length=200)
    Goal_date = models.DateTimeField('Goal created')
    entry = models.TextField(max_length=200, null = True)
    def __str__(self):
        return self.goal_title
class Workouts(models.Model):
    # ...
    workout_title = models.CharField(max_length=200)
    Goal_date = models.DateTimeField('Goal created')
    entry = models.TextField(max_length=200, null = True)
    def __str__(self):
        return self.goal_title