from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
<<<<<<< HEAD
    weight = models.IntegerField(null=True)
    bmi = models.IntegerField(null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/')
=======
    weight = models.IntegerField(null=True, blank=True)
    bmi = models.IntegerField(null=True, blank=True)
    fav_exercise = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile/')
    points_total = models.IntegerField(default=0)
>>>>>>> points

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


class Goal(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    reach_date = models.DateTimeField('reach date')
    goal_text = models.TextField(max_length=50, blank = True, null=True)
    accomplished = models.BooleanField('have accomplished')
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def get_absolute_url(self):
        return reverse('goals list')


class Workout(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    workout_title = models.CharField(max_length=200)
    workout_type = models.CharField(max_length=200)
    workout_description = models.TextField(max_length=500)
    points = models.IntegerField(default=0)
    date = models.DateTimeField('Workout Completed', null = True, blank = True)
    def __str__(self):
        return self.workout_title

class MyWorkout(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    myworkout_title = models.CharField(max_length=200)
    myworkout_description = models.TextField(max_length=500)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.workout_title

<<<<<<< HEAD
class MyExercise(models.Model):
    myworkout = models.ForeignKey(MyWorkout, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    information = models.TextField(max_length=500)    information = models.TextField(max_length=500)
=======

class GraphMaker(models.Model):
    date = models.DateField('date')
    value = models.IntegerField('value', null=False, blank=False)
>>>>>>> points
