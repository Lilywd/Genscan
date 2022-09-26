from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  SetPasswordForm
from .models import Profile
# Create your forms here.

class ContactForm(forms.Form):
	first_name = forms.CharField (widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'First name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Last name'}))
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'name@example.com'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'class': 'iinput-field', 'cols':'20', 'placeholder':'Your message...'}))


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Username'}))
    first_name = forms.CharField (widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Last name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'email@example.com'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
   

    class Meta:
        model = Profile
        fields = ['avatar']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

