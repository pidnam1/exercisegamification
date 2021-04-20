from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(null=True, blank=True)
    bmi = models.IntegerField(null=True, blank=True)
    fav_exercise = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile/')
    points_total = models.IntegerField(default=0)


    friends = models.ManyToManyField(User, blank=True, related_name='friends')

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


STATUS_CHOICES = (
    ('pending', 'pending'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='pending')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


'''
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('friend_request_list')


class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE())
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, user):
        if user not in self.friends.all():
            self.friends.add(user)
            self.save()

    def remove_friend(self, user):
        if user in self.friends.all():
            self.friends.remove(user)

    def unfriend(self, removee):
        self.remove_friend(removee)
        friends_list = FriendsList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual(self, friend):
        if friend in self.friends.all():
            return True
        else:
            return False



class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE(), related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE(), related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendsList.object.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendsList.object.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

'''
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
    date = models.DateField('Workout Completed', null = True, blank = True)
    def __str__(self):
        return self.workout_title


class MyWorkout(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    myworkout_title = models.CharField(max_length=200)
    myworkout_description = models.TextField(max_length=500)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.workout_title


class MyExercise(models.Model):
    myworkout = models.ForeignKey(MyWorkout, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    information = models.TextField(max_length=500)


class GraphMaker(models.Model):
    date = models.DateField('date')
    value = models.IntegerField('value', null=False, blank=False)

