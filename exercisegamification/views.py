from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm, AddGoalForm
from .models import Profile, Goal
# Create your views here.

def profilePage(request):

    ## Gets current user
    user = request.user
    user.save()

    ## Loads a profile instance
    user.refresh_from_db()

    ## Saves profile instance
    user.profile.save()
    user.save()

    ## Calls our profile model of specific user
    loggedProfile = user.profile
    goals_list = loggedProfile.goal_set.all()

    return render(request, "exercisegamification/profile.html", {"profile": loggedProfile,"goals_list": goals_list})
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


        req_form = EditProfileForm(request.POST, request.FILES)
        if req_form.is_valid():

            ## Saves all the filled out form values to the profile
            loggedProfile.first_name = req_form.cleaned_data.get('first_name')
            loggedProfile.last_name = req_form.cleaned_data.get('last_name')
            loggedProfile.age = req_form.cleaned_data.get('age')
            loggedProfile.weight = req_form.cleaned_data.get('weight')
            loggedProfile.bmi = req_form.cleaned_data.get('bmi')
            loggedProfile.fav_exercise = req_form.cleaned_data.get('fav_exercise')
            loggedProfile.profile_pic = req_form.cleaned_data.get('profile_pic')
            loggedProfile.save()

            return redirect('/profile/')
    else:
        req_form = EditProfileForm(initial = {'first_name':loggedProfile.first_name, 'last_name': loggedProfile.last_name, 'age'
                                          :loggedProfile.age, 'weight': loggedProfile.weight, 'bmi': loggedProfile.bmi,
                                              'fav_exercise': loggedProfile.fav_exercise, 'profile_pic': loggedProfile.profile_pic})
        args = {'req_form': req_form}
        return render(request, 'exercisegamification/edit_profile.html', args)


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