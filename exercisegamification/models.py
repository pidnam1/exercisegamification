from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(null=True)
    bmi = models.IntegerField(null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/')

    public = models.BooleanField(default=False)
    private = models.BooleanField(default=True)

    @property
    def is_private(self):
        return self.private

    @property
    def is_public(self):
        return self.public

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

class Profile_opt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(null=True)
    bmi = models.IntegerField(null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/')


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