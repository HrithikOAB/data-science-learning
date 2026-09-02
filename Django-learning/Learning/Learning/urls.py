"""
URL configuration for Learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Main.urls')),

    # DRF tutorial apps — each style lives at its own prefix so students
    # can compare them side-by-side.
    # path('api/fbv/',      include('api_fbv.urls')),      # function-based views
    # path('api/apiview/',  include('api_apiview.urls')),  # class-based APIView
    # path('api/generics/', include('api_generics.urls')), # generic views
    # path('api/viewset/',  include('api_viewset.urls')),  # ModelViewSet + Router
]
