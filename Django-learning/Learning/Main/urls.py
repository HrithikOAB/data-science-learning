from django.urls import path
from .views import *
urlpatterns = [
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),






    path('profile/', profile_page, name='profile'),

    

    path('edit-profile/', edit_profile, name='edit_profile'),

    path('logout', logout_view, name='logout'),
    
    
]
