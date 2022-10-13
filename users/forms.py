from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Username'}))
    first_name = forms.CharField (widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'name@example.com'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'iinput-field', 'placeholder':'Password'}))
    password2 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'iinput-field', 'placeholder':'Confirm yourPassword'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class UserAuthenticationForm(forms.ModelForm):
    # username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'name@example.com'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'iinput-field', 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ( 'email', 'password')

    def clean(self):
        if self.is_valid():
            # username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid login")


class UserUpdateForm(forms.ModelForm):
    
	class Meta:
		model = User
		fields = ('email', 'username', )

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % user)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


class ContactForm(forms.Form):
	first_name = forms.CharField (widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'First name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'Last name'}))
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'iinput-field', 'placeholder':'name@example.com'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'class': 'iinput-field', 'cols':'20', 'placeholder':'Your message...'}))

