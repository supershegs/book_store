from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class AssignUserPathMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', None)  
        path = request.path_info   

        if auth_header is not None and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                validated_token = JWTAuthentication().get_validated_token(token)
                user = JWTAuthentication().get_user(validated_token)
                print(f"{user.username} with {user.role} role")
                
                if path.startswith('/api/v1/user/') and user.role != 'user':
                    return JsonResponse(
                        {'errorFlag': 'true', 'statusCode': '99', 'statusMsg': 'Access forbidden: Users only'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                if path.startswith('/api/v1/admin/') and user.role != 'admin':
                    return JsonResponse(
                        {'errorFlag': 'true', 'statusCode': '99', 'statusMsg': 'Access forbidden: Admins only'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                if user.role not in ['user', 'admin']:
                    return JsonResponse(
                        {'errorFlag': 'true', 'statusCode': '99', 'statusMsg': 'User not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

            except InvalidToken:
                return JsonResponse(
                    {'errorFlag': 'true', 'statusCode': '98', 'statusMsg': 'Invalid token provided'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except AuthenticationFailed:
                return JsonResponse(
                    {'errorFlag': 'true', 'statusCode': '98', 'statusMsg': 'Authentication failed'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

        response = self.get_response(request)
        return response
