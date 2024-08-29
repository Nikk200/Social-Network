from django.shortcuts import render
import io, json
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSignUpSerializer, UserSignInSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser


@api_view()
def test_get(request):
    if isinstance(request.user, AnonymousUser):
        return Response({"message": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "User is logged in", "user": request.user.username}, status=status.HTTP_200_OK)

@api_view(['POST'])
def sign_up_user(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    python_data = JSONParser().parse(stream)
    serializer = UserSignUpSerializer(data=python_data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": f'Signup success for {user.email}'}, status = status.HTTP_201_CREATED)
    
    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def sign_in_user(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    python_data = JSONParser().parse(stream)
    serializer = UserSignInSerializer(data=python_data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email.lower(), password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
    return Response({"message": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


