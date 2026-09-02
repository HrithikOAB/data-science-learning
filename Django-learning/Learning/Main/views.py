from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Person
import random
from django.contrib.auth import authenticate, login, logout

# Create your views here.



def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request,'login.html')


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user = Person.objects.create(name=name, email=email, number=mobile,username=email)

        user.set_password(password)
        user.save()
        return redirect('login')
    else:
        return render(request,'signup.html')




def profile_page(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('login')




def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')
    return render(request,'edit-profile.html')


def logout_view(request):
    logout(request)
    return redirect('login')