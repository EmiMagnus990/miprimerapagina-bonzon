from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=30, required=False)
    last_name = forms.CharField(label="Apellido", max_length=30, required=False)
    email = forms.EmailField(label="Email", required=False)
    username = forms.CharField(label="Nombre de usuario", max_length=150, required=True)

    class Meta:
        model = Profile
        fields = []