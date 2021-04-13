from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from .forms import EditProfileForm, AddGoalForm, AddMyWorkoutForm, EditGoalForm, WorkoutDateForm
from .models import Profile, Goal, Workout, MyWorkout, Relationship
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def profilePage(request, pk=None):
    rel_receiver = []
    rel_sender = []
    if pk:
        loggedProfile = Profile.objects.get(pk=pk)
        user = request.user.profile
        rel_r = Relationship.objects.filter(sender=user)
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        rel_s = Relationship.objects.filter(receiver=user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

    else:
        loggedProfile = request.user.profile

    '''## Gets current user
    #user = request.user
    user.save()

    ## Loads a profile instance
    user.refresh_from_db()

    ## Saves profile instance
    user.profile.save()
    user.save()'''

    ## Calls our profile model of specific user
    #loggedProfile = user.profile
    goals_list = loggedProfile.goal_set.all()
    workouts_list = loggedProfile.workout_set.all()
    friend_requests = Relationship.objects.invatations_received(loggedProfile)
    for w in workouts_list:
        loggedProfile.points_total += w.points
    loggedProfile.save()

    return render(request, "exercisegamification/profile.html", {"profile": loggedProfile,"goals_list": goals_list, 'friend_requests':
                                                                 friend_requests, 'rel_sender': rel_sender, 'rel_receiver': rel_receiver, "workouts_list": workouts_list})

    #return render(request, "exercisegamification/profile.html", {"profile": loggedProfile,"goals_list": goals_list})
# /***************************************************************************************
# *  REFERENCES
# *  Title: edit profile
# *  Author: Max Goodridge
# *  Date: 04/04/2021
# *  
# *  URL: https://www.youtube.com/watch?v=D9Xd6jribFU&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=19
# *
# *  Title: Basic edit profile
# *
# ***************************************************************************************/
def edit_profile(request):
    loggedProfile = Profile.objects.get(user=request.user)

    if request.method == 'POST':


        req_form = EditProfileForm(request.POST)
        if req_form.is_valid():

            ## Saves all the filled out form values to the profile
            loggedProfile.first_name = req_form.cleaned_data.get('first_name')
            loggedProfile.last_name = req_form.cleaned_data.get('last_name')
            loggedProfile.age = req_form.cleaned_data.get('age')
            loggedProfile.weight = req_form.cleaned_data.get('weight')
            loggedProfile.bmi = req_form.cleaned_data.get('bmi')
            loggedProfile.save()

            return redirect('/profile/')
    else:
        req_form = EditProfileForm(initial = {'first_name':loggedProfile.first_name, 'last_name': loggedProfile.last_name, 'age'
                                          :loggedProfile.age, 'weight' : loggedProfile.weight, 'bmi' : loggedProfile.bmi})
        args = {'req_form': req_form}
        return render(request, 'exercisegamification/edit_profile.html', args)


def find_friends(request):
    return render(request, 'exercisegamification/find_friends.html', {'users': Profile.objects.all()})


def send_friend_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='pending')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')


def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')


def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'pending':
            rel.status = 'accepted'
            rel.save()
    return redirect('profile')


def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profile')
'''
@login_required
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    if to_user not in from_user.friends.all() and from_user not in to_user.friends.all():
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request already sent')


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')
'''

# /***************************************************************************************
# *  REFERENCES
# *  Title: Add Blog Posts to Django Webpage
# *  Author: Codemy.com
# *  Date: 04/05/2021
# *
# *  URL: https://www.youtube.com/watch?v=CnaB4Nb0-R8
# *
# ***************************************************************************************/
class GoalsView(generic.ListView):
    model = Goal
    template_name = 'exercisegamification/goals_list.html'
    context_object_name = 'goals_list'
    def get_queryset(self):
        return Goal.objects.all()

#class GoalDetailView(generic.DetailView):
#    model = Goal
#    template_name = 'exercisegamification/goal_detail.html'

def GoalDetailView(request,pk):
    loggedProfile = Profile.objects.get(user=request.user)
    goal = loggedProfile.goal_set.get(pk=pk)
    return render(request, "exercisegamification/goal_detail.html", {"profile": loggedProfile,"goal": goal})

#class AddGoalView(generic.CreateView):
#    model = Goal
#    #form_class = GoalForm
#    template_name = 'exercisegamification/add_goal.html'
#    fields = '__all__'

def AddGoalView(request):
    loggedProfile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        req_form = AddGoalForm(request.POST)
        if req_form.is_valid():
            goal = Goal(author=loggedProfile)
            goal.title = req_form.cleaned_data.get('title')
            goal.pub_date = req_form.cleaned_data.get('pub_date')
            goal.reach_date = req_form.cleaned_data.get('reach_date')
            goal.goal_text = req_form.cleaned_data.get('goal_text')
            goal.accomplished = req_form.cleaned_data.get('accomplished')
            goal.save()

            return redirect('/profile/')
    else:
        req_form = AddGoalForm()
        args = {'req_form': req_form}
        return render(request, 'exercisegamification/add_goal.html', args)

def EditGoalView(request,pk):
    loggedProfile = Profile.objects.get(user=request.user)
    goal = loggedProfile.goal_set.get(pk=pk)
    if request.method == 'POST':
        req_form = EditGoalForm(request.POST)
        if req_form.is_valid():
            goal = loggedProfile.goal_set.get(pk=pk)
            goal.title = req_form.cleaned_data.get('title')
            goal.pub_date = req_form.cleaned_data.get('pub_date')
            goal.reach_date = req_form.cleaned_data.get('reach_date')
            goal.goal_text = req_form.cleaned_data.get('goal_text')
            goal.accomplished = req_form.cleaned_data.get('accomplished')
            goal.save()

            return redirect('/profile/')
    else:
        req_form = EditGoalForm(initial={'title':goal.title, 'pub_date': goal.pub_date, 'reach_date':
            goal.reach_date, 'goal_text': goal.goal_text, 'accomplished': goal.accomplished})
        args = {'req_form': req_form}
        return render(request, 'exercisegamification/edit_goal.html', args)

def SelectWorkout(request):
    workouts_list = Workout.objects.filter(author = None)
    return render(request, "exercisegamification/select_workout.html", {"workouts_list": workouts_list})


def WorkoutDetailView(request, pk):
    loggedProfile = Profile.objects.get(user=request.user)
    workout = Workout.objects.get(pk=pk)
    if request.method == 'POST':
        req_form = WorkoutDateForm(request.POST)
        if req_form.is_valid():
            added_workout = Workout(author = loggedProfile)
            added_workout.workout_title = workout.workout_title
            added_workout.workout_type = workout.workout_type
            added_workout.workout_description = workout.workout_description
            added_workout.points = workout.points
            added_workout.date = req_form.cleaned_data.get('date')
            added_workout.save()

            return redirect('/profile/')
    else:
        req_form = WorkoutDateForm
        args = {'req_form': req_form}
    return render(request, "exercisegamification/workout_detail.html", {"workout": workout, "req_form": req_form})



class MyWorkoutView(generic.ListView):
    model = MyWorkout
    template_name = 'exercisegamification/myworkouts_list.html'
    context_object_name = 'myworkouts_list'
    def get_queryset(self):
        return MyWorkout.objects.all()

def AddMyWorkoutView(request):
    loggedProfile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        req_form = AddMyWorkoutForm(request.POST)
        if req_form.is_valid():
            myworkout = MyWorkout(author=loggedProfile)
            myworkout.myworkout_title = req_form.cleaned_data.get('workout_title')
            myworkout.myworkout_description = req_form.cleaned_data.get('workout_description')


def MyWorkoutDetailView(request,pk):
    loggedProfile = Profile.objects.get(user=request.user)
    myworkout = loggedProfile.goal_set.get(pk=pk)
    return render(request, "exercisegamification/myworkout_detail.html", {"profile": loggedProfile,"myworkout": myworkout})
            


