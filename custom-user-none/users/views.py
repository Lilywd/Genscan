from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm, UpdateUserForm, UpdateProfileForm, SetPasswordForm
from qrcode import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator





# Create your views here.
def landing(request):
    return render(request, 'users/landing.html')


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']

        if User.objects.filter(username=username):
            messages.error(request, "username already exists, please try something else")
            return redirect('/')

        if User.objects.filter(email=email):
            messages.error(request, "email already exists, please login")
            return redirect('signin')
        
        if len(username)>15:
            messages.error(request, "username is too long, please try something else")
        
      
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

       
        myuser.save()
        

        messages.success(request, "Please Confirm your email to complete registration")
        
        # welcome email
        subject = "welcome to genscan!"
        message = "hello" + myuser.first_name + "!! \n" +  "Welcome to Genscan! \n Thank you for visiting our website. \n We have sent you a confirmation email to confirm your email, please confirm your email address in order to activate you account.  \n\n Thank you. "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')
    
    return render(request, 'users/register.html')
  
# def activateEmail(request, user, to_email):
#     mail_subject = 'Activate your user account.'
#     message = render_to_string('template_activate_account.html', {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#             received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and account_activation_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('signin')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
    
        if user is not None:
            login(request, user)
            fname= user.first_name
            messages.info(request, f"You are now logged in as {username}.")
            
            return render(request,  'users/landing.html',{'fname':fname})
			
        else:
            messages.error(request, user, "incorrect credentials")
            
            return redirect('/')
    return render(request, 'users/signin.html')


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('signin')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password/password_reset_confirm.html', {'form': form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "users/password/password_reset_email.txt"
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
						send_mail(subject, email, 'ndungulilianwanjiku@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required
def signout(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect('/')
    
@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect(to='/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
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
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent")
            return redirect ('/')
            messages.error(request, "Error Message not sent")
    
    form = ContactForm()
    return render(request, 'users/contact.html', {'form':form})


@login_required
def changeemail(request):
    return render(request, 'users/changeemail.html')