from django.contrib import admin
from .models import Profile, Goal, Workout

# Register your models here.
admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Workout)