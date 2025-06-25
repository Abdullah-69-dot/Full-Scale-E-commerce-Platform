from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.core.exceptions import ValidationError



class UserRegisterForm(UserCreationForm):
    username = forms.CharField( widget = forms.TextInput(attrs={"placeholder": 'Username'}))
    email = forms.EmailField( widget = forms.EmailInput(attrs={"placeholder": 'Email'}))
    password1 = forms.CharField( widget = forms.PasswordInput(attrs={"placeholder": 'Password'}))
    password2 = forms.CharField( widget = forms.PasswordInput(attrs={"placeholder": 'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email already exists")
    #     return email



class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full_name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']


