
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    Publisher, 
    Category, 
)

CustomUser = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {
            'email': {'required': True},  
            'username': {'required': True},
            'first_name': {'required': True},  
            'last_name': {'required': True},   
            'role': {'required': False},       
            'password': {'required': True},    
        } 
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data.get('role', CustomUser.USER),  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
    
    
class CustomAdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'role']
        
        extra_kwargs = {
            'email': {'required': False},  
            'username': {'required': True},
            'first_name': {'required': False},  
            'last_name': {'required': False},   
            'role': {'required': False},       
            'password': {'required': True},    
        }
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', CustomUser.ADMIN),  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

