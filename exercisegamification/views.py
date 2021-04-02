from django.shortcuts import render

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