from django.contrib import admin
from .models import Profile, Goal, Relationship
from .models import Profile, Goal, Workout, PointAchievement, GoalAchievement

# Register your models here.
admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Relationship)
admin.site.register(PointAchievement)
admin.site.register(GoalAchievement)

'''
class FriendListAdmin():
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendsList


admin.site.register(FriendsList)
admin.site.register(FriendRequest)
'''
admin.site.register(Workout)