from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm, AddGoalForm, AddMyWorkoutForm
from .models import Profile, Goal, Workout, MyWorkout
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
    #myworkouts_list = 

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



def SelectWorkout(request):
    workouts_list = Workout.objects.filter(author = None)
    return render(request, "exercisegamification/select_workout.html", {"workouts_list": workouts_list})


def WorkoutDetailView(request, pk):
    workout = Workout.objects.get(pk=pk)
    return render(request, "exercisegamification/workout_detail.html", {"workout": workout})



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
            


