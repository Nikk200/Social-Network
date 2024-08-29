from django.shortcuts import render
import io, json
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSignUpSerializer


@api_view()
def test_get(request):
    return Response({"data": "This is get request"})

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



