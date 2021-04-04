from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from accounts.forms import EditProfileForm
# Create your views here.

def profilePage(request):

    user = request.user
    user.save()
    user.refresh_from_db()

    user.profile.age = 22
    user.profile.name = "Mandip"
    user.profile.save()
    user.save()

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
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('exercisegamification/profile.html')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'exercisegamification/edit_profile.html', args)