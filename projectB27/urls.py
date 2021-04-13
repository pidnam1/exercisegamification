"""projectB27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from exercisegamification import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='exercisegamification/index.html'), name='login'),
    path('admin/', admin.site.urls),
    path('profile/', views.profilePage, name="profile"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
    #path('profile/goals/', views.profilePage, name = "profile"),
    #path('profile/workouts/', views.profilePage, name = "profile"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('goals/', views.GoalsView.as_view(), name='goals list'),
    path('goals/<int:pk>', views.GoalDetailView, name='goal detail'),
    path('goals/create/', views.AddGoalView, name='add goal'),
    path('goals/edit/<int:pk>', views.EditGoalView, name='edit goal'),
    path('workout/<int:pk>', views.WorkoutDetailView, name = 'add workout'),
    path('workout/', views.SelectWorkout, name = 'select workout'),
    path('myworkouts/', views.MyWorkoutView.as_view(), name = 'myworkouts list'),
    path('myworkouts/<int:pk>', views.MyWorkoutView.as_view(), name = 'myworkout detail')
]
