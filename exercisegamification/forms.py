from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Field
from .models import Profile

class EditProfileForm(ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    age = forms.IntegerField(max_value=None,min_value=0, label="Age")

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'age'
        )