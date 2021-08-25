from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import message, send_mail
from django.contrib.auth import login,authenticate,logout


def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('LOGIN')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.info(request,'User Not Found')
            return redirect('LOGIN')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.info(request,'Your account is not verified')
            return redirect('LOGIN')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.info(request,'Wrong username and password')
            return redirect('LOGIN')
        else:
            messages.success(request,'Logged In')
            login(request,user)
            return render(request,'home.html',{'user':user})

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('LOGIN')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            if User.objects.filter(username=username).first():
                messages.info(request,'User Name is already Exist!')
                return redirect('REGISTER')
        
            if User.objects.filter(email=email).first():
                messages.info(request,'Email addres is already Exist!')
                return redirect('REGISTER')

            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            sendMail(email,auth_token)
            return redirect('TOKENSEND')
        except Exception as e:
            print(e)
    return render(request,'register.html')

def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'tokensend.html')

def sendMail(email,token):
    subject = 'Verification Mail'
    message = f"Hello, Please paste the link to verify your account http://127.0.0.1:8000/verify/{token} "
    email_from = settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your Account is already Verified')
                return redirect('LOGIN')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your Account has been verified')
            return redirect('LOGIN')
        else:
            return redirect('ERROR')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'error.html')

