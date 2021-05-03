from __future__ import print_function

from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm, AddGoalForm, EditGoalForm
from .models import Profile, Goal, Relationship
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, AddGoalForm, AddMyWorkoutForm, EditGoalForm, WorkoutDateForm
from .models import Profile, Goal, Workout, MyWorkout, PointAchievement
from email.mime.text import MIMEText
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
# Create your views here.


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    credentials = creds
    service = build('gmail', 'v1', credentials=creds)
    return service
def LoginView(LogInView):
    if LogInView.user.is_authenticated:
        loggedProfile = LogInView.user.profile
        friends = loggedProfile.friends.all()
        workouts = []
        for f in friends:
            try:
                workouts.append(f.profile.workout_set.latest('date'))
            except:
                pass
        return render(LogInView, "exercisegamification/index.html", {'profile':loggedProfile, "friends": friends, "workouts": workouts})

    else:
        return render(LogInView, "exercisegamification/index.html")
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
    friend_requests = Relationship.objects.invatations_received(loggedProfile)
    workouts_list = loggedProfile.workout_set.all()
    achievementQuerySet = PointAchievement.objects.filter(author__isnull=True)
    #achievement = achievementQuerySet.get()
    users_achievements = loggedProfile.pointachievement_set.all()
    
    loggedProfile.points_total = 0
    for w in workouts_list:
        loggedProfile.points_total += w.points
    loggedProfile.save()
    for achievement in achievementQuerySet:
        if loggedProfile.points_total >= achievement.achievement_threshold:
            if users_achievements.count() == 0:
                PointAchievement.objects.create(author=loggedProfile, achievement_threshold=achievement.achievement_threshold, achievement_text=achievement.achievement_text, achievement_title=achievement.achievement_title)
            #for a in users_achievements:
            if users_achievements.filter(achievement_title=achievement.achievement_title).exists():
                pass
            else:
                PointAchievement.objects.create(author=loggedProfile, achievement_threshold=achievement.achievement_threshold, achievement_text=achievement.achievement_text, achievement_title=achievement.achievement_title)


    return render(request, "exercisegamification/profile.html", {"profile": loggedProfile,"goals_list": goals_list, "workouts_list": workouts_list,'friend_requests':
        friend_requests, 'rel_sender': rel_sender, 'rel_receiver': rel_receiver})

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


def find_friends(request):
    return render(request, 'exercisegamification/find_friends.html', {'users': Profile.objects.all()})

def leaderboard(request):
    return render(request, 'exercisegamification/Leaderboard.html', {'users': Profile.objects.order_by('-points_total')[:10]})

#class LeaderboardView(generic.ListView):

#friends
def send_friend_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)

        friend_string = receiver.user.username
        message_body = "Hi " + friend_string + "! You just received a friend request from " + sender.user.username + "! Go to https://project-b27.herokuapp.com/ to accept the request!" 
        message = create_message("exercisegamificationb27@gmail.com", receiver.user.email, "New Friend Request" , message_body)
        print(receiver.user.email)
        service = get_service()
        send_message(service, "exercisegamificationb27@gmail.com", message)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='pending')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')

#friends
def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)



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

#friends
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

#friends
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profile')

# /***************************************************************************************
# *  REFERENCES
# *  Title: Add Blog Posts to Django Webpage
# *  Author: Codemy.com
# *  Date: 04/05/2021
# *
# *  URL: https://www.youtube.com/watch?v=CnaB4Nb0-R8
# *
# ***************************************************************************************/
#goals
class GoalsView(generic.ListView):
    model = Goal
    template_name = 'exercisegamification/goals_list.html'
    context_object_name = 'goals_list'
    def get_queryset(self):
        return Goal.objects.all()

#class GoalDetailView(generic.DetailView):
#    model = Goal
#    template_name = 'exercisegamification/goal_detail.html'
#goals
def GoalDetailView(request, pk, pi=None):
    if pi:
        loggedProfile = Profile.objects.get(pk=pi)
    else:
        loggedProfile = Profile.objects.get(user=request.user)
    goal = loggedProfile.goal_set.get(pk=pk)
    return render(request, "exercisegamification/goal_detail.html", {"profile": loggedProfile,"goal": goal})
#goals
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
#goals
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

#goals
def DeleteGoalView(request,pk):
    goal = Goal.objects.get(pk=pk)
    goal.delete()
    #return HttpResponseRedirect('profile')
    return redirect('/profile/')

#workouts
def SelectWorkout(request):
    workouts_list = Workout.objects.filter(author = None)
    return render(request, "exercisegamification/select_workout.html", {"workouts_list": workouts_list})

#workouts
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


#workouts
class MyWorkoutView(generic.ListView):
    model = MyWorkout
    template_name = 'exercisegamification/myworkouts_list.html'
    context_object_name = 'myworkouts_list'
    def get_queryset(self):
        return MyWorkout.objects.all()
#workouts
def AddMyWorkoutView(request):
    loggedProfile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        req_form = AddMyWorkoutForm(request.POST)
        if req_form.is_valid():
            myworkout = MyWorkout(author=loggedProfile)
            myworkout.myworkout_title = req_form.cleaned_data.get('workout_title')
            myworkout.myworkout_description = req_form.cleaned_data.get('workout_description')

#workouts
def MyWorkoutDetailView(request,pk):
    loggedProfile = Profile.objects.get(user=request.user)
    myworkout = loggedProfile.goal_set.get(pk=pk)
    return render(request, "exercisegamification/myworkout_detail.html", {"profile": loggedProfile,"myworkout": myworkout})

#achievements
def AchievementsView(request):
    loggedProfile = Profile.objects.get(user=request.user)
    #achievement = Achievement.objects.get(pk=pk)
    #if loggedProfile.points_total >= achievement.achievement_threshold:
    achievements_list = loggedProfile.pointachievement_set.all()
    return render(request, "exercisegamification/achievements.html", {"profile": loggedProfile,"achievements_list": achievements_list})


