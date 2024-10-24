from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomUserRegistrationSerializer,
    CustomAdminRegistrationSerializer
) 



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)        
        try:
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data  
            
            new_access_token = tokens.get('access')
            validated_token = JWTAuthentication().get_validated_token(new_access_token)
            user = JWTAuthentication().get_user(validated_token)
            print(f"{user.username} with {user.role} role")
                      
            response_data = {
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'errorFlag': 'false',
                'statusCode': '00',
                'statusMsg': 'New token created'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errorFlag': 'true', 'statusCode': '99', 'statusMsg': 'Token generation failed', 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True) 
            tokens = serializer.validated_data
            
            new_access_token = tokens.get('access')
            validated_token = JWTAuthentication().get_validated_token(new_access_token)
            user = JWTAuthentication().get_user(validated_token)
            print(f"{user.username} with {user.role} role") 
            
            response_data = {
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'errorFlag': 'false',
                'statusCode': '00',
                'statusMsg': 'Refresh token generated successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errorFlag': 'true', 'statusCode': '99', 'statusMsg': 'Refresh token generation failed', 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        

class CustomUserRegistrationView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'statusCode': '00',
                'statusMsg': 'User registered successfully',
            }, status=status.HTTP_201_CREATED)
        return Response({
            'errorFlag': 'true',
            'statusCode': '99',
            'statusMsg': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomAdminRegistrationView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CustomAdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'username': user.username,
                'role': user.role,
                'statusCode': '00',
                'statusMsg': 'Admin registered successfully',
            }, status=status.HTTP_201_CREATED)
        return Response({
            'errorFlag': 'true',
            'statusCode': '99',
            'statusMsg': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)