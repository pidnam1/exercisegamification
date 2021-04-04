from django.shortcuts import render
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
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
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('exercisegamification/profile.html')
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'exercisegamification/edit_profile.html', args)