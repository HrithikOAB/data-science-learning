from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from Main.models import Person
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PersonSerializer
# Create your views here.


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if Person.objects.filter(email=email).exists():
        if Person.objects.get(email=email).check_password(password):
            user = Person.objects.get(email=email)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    
    return Response({'error': 'Invalid credentials'}, status=401)



@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})



@api_view(['POST'])
def register_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if Person.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = Person.objects.create_user(username=email, email=email, password=password)
  
    return Response({'response': 'User registered successfully'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = PersonSerializer(request.user)
    return Response(serializer.data)
