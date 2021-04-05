from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm
from .models import Profile
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

    return render(request, "exercisegamification/profile.html", {"profile": loggedProfile})
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


        form = EditProfileForm(request.POST)
        if form.is_valid():

            ## Saves all the filled out form values to the profile
            loggedProfile.first_name = form.cleaned_data.get('first_name')
            loggedProfile.last_name = form.cleaned_data.get('last_name')
            loggedProfile.age = form.cleaned_data.get('age')
            loggedProfile.save()

            return redirect('/profile/')
    else:
        form = EditProfileForm(initial = {'first_name':loggedProfile.first_name, 'last_name': loggedProfile.last_name, 'age'
                                          :loggedProfile.age})
        args = {'form': form}
        return render(request, 'exercisegamification/edit_profile.html', args)