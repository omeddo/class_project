from email import message
from django.shortcuts import redirect, render
from accounts.models import Account
from .forms import RegistrationForm
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required

# verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def register(request):
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         first_name = form.cleaned['first_name']
         last_name = form.cleaned['last_name']
         email = form.cleaned['email']
         phone_number = form.cleaned['phone_number']
         password = form.cleaned['password']
         username =email.split("@")[0]
         
         user = Account.object.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
         user.phone_number=phone_number
         user.save()
         
         # USER ACTIVATION
         current_site = get_current_site(request)
         mail_subject= 'Please activate your account'
         message= render_to_string('accounts/account_verfication_email.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
         })
         to_email=email
         send_email=EmailMessage(mail_subject,message,to=[to_email])
         send_email.send()
         messages.success(request, 'Registration Successful.')
         return redirect('register')
   else:
      form = RegistrationForm()
   context = {
   'form' : form,
   }
   
   return render(request, 'accounts/register.html',context)

def login(request):
   if request.method =='POST':
      email = request.POST['email']
      password = request.POST['password']
      
      user = auth.authenticate(email=email,password=password)
      
      if user is not None:
         auth.login(request,user)
         # message.success(request,'you are logged in')
         return redirect('home')
      else:
         message.error(request,'Invalid login credentials')
         return redirect('login')
         
   return render(request, 'accounts/login.html')

@login_required(login_url ='login')

def logout(request):
   auth.logout(request)
   message.success(request,'you are logged out')
   return redirect('login')