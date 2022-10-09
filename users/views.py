from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from genscan.models import QrCode
from users.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm,ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from users.models import User
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required



# Create your views here.
def landing(request):
    return render(request, 'users/landing.html')


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email,password=raw_password)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect("/")
            # login(request,user)
            # messages.success(request, f"New account created: {user.username}")
            # return redirect ("signin")
           
        else:
            context={'registration_form':form}
            messages.error(request,  "Account not created")
    else: # GET request
        form = RegistrationForm()
        context={'registration_form':form}

    return render(request, 'users/register.html', context)


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user} please go to you email {to_email}inbox and click on \
            received activation link to confirm and complete the registration. Note:Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
   
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('signin')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')





def signin(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("/")

	if request.POST:
	
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				messages.info(request, f"You are now logged in as {user}.")
				return redirect("/")

			else:
				messages.error(request, user, "incorrect credentials")


	else:
		form = UserAuthenticationForm()
		

	context['signin_form'] = form
	if 'next' in request.POST:
		return redirect(request.POST['next'])
	# print(form)
	return render(request, "users/signin.html", context)


def signout(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect('/')


@login_required(login_url='/signin')
def profile(request):

	if not request.user.is_authenticated:
			return redirect("signin")

	context = {}
	if request.POST:
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			messages.success(request, 'Your profile has been updated successfully')
			

		else:
			messages.error(request,  "Error")
	else:
		form = UserUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['profile_form'] = form

	qrcode = QrCode.objects.all()
	


	return render(request, "users/profile.html", context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
            message = "\n".join(body.values())

            try:
                from_email = settings.EMAIL_HOST_USER 
                send_mail(subject, message, from_email, ['admin@example.com'], fail_silently=True)
                
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent")
            return redirect ('/')
            messages.error(request, "Error Message not sent")
    
    form = ContactForm()
    return render(request, 'users/contact.html', {'form':form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "users/password/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form":password_reset_form})