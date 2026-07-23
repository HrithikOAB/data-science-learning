from django.urls import path
from .views import *
urlpatterns = [
    path('login', login_page,name='login'),
    path('otp-send', otp_send, name='otp_send'),

    path('otp-verify', otp_verify,name='verify_otp'),
    path('resend-otp', resend_otp,name='resend_otp'),


    path('profile',profile_page,name='profile'),
    path('edit-profile',profile_page,name='edit_profile'),
    path('edit-profile',profile_page,name='change_password'),
    path('edit-profile',profile_page,name='logout'),
    
]
