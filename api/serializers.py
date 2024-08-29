from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def validate_first_name(self, value):
        if not value:
            raise ValidationError("First name is required for creating the user  as the name will be required while searching for other users.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise ValidationError("Last name is required for creating the user  as the name will be required while searching for other users.")
        return value
    

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise ValidationError("An account with this email is already registered.")
        return value.lower()
    
    def create(self, validated_data):
        print("validated_data >> ", validated_data)
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['email'],
            password = validated_data['password']
        )
        return user



class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    

    def validate(self, data):
        email = data['email'].lower()
        password = data['password']

        user = authenticate(username=email, password=password)
        if user is None:
            raise ValidationError("Invalid credentials.")
        return data
        









