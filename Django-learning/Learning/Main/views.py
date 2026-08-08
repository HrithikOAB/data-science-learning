from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Person
import random
# Create your views here.
def login_page(request):
    return render(request,'login.html')



def otp_send(request):
    number = request.POST.get('email_or_mobile')
    otp = random.randint(0000,9999)
    if Person.objects.filter(number=number).exists():
        person_info = Person.objects.get(number=number)
        person_info.otp = otp
        person_info.save()

    else:
        Person.objects.create(number=number,otp=otp).save()        
    return render(request,'otp-verify.html',{'user_number':number,'message':'Enter your otp'})



def otp_verify(request):
    user_otp = request.POST.get('otp')
    number = request.POST.get('user_number')

    
    if Person.objects.filter(number=number,otp=user_otp).exists():
         return redirect('profile')
    else:
        return HttpResponse('Wrong OTP')


def resend_otp(request):
    number = request.POST.get('user_number')
    otp = random.randint(0000,9999)
    if Person.objects.filter(number=number).exists():
            person_info = Person.objects.get(number=number)
            person_info.otp = otp
            person_info.save()
    
    else:
            Person.objects.create(number=number,otp=otp).save()  
    return render(request,'otp-verify.html')


def profile_page(request):
    
    return render(request,'profile.html')