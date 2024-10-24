from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    BookStore,
    BooksBorrowed,
    CustomUser
)

from common.serializers import (
    PublisherSerializer,
    CategorySerializer
)



class BookStoreSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = BookStore
        fields = ['id', 'title', 'author', 'publisher', 'categories', 'published_date', 'available_copies']

        extra_kwargs = {
            'title': {'required': True},  
            'author': {'required': True},
            'publisher': {'required': True},  
            'categories': {'required': True},   
            'published_date': {'required': True},       
            'available_copies': {'required': True},    
        }
class BooksBorrowedSerializer(serializers.ModelSerializer):
    return_date = serializers.SerializerMethodField()
    class Meta:
        model = BooksBorrowed
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date', 'duration_days']

    def get_return_date(self, obj):
        return obj.return_date.date() 
    
# class UserSerializer(serializers.ModelSerializer):
#     borrowed_books = BooksBorrowedSerializer(many=True, source='borrowedbook_set')

#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'email', 'borrowed_books']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['id', 'username']
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ListBorrowedBookSerializer(serializers.ModelSerializer):
    book = BookStoreSerializer(read_only=True)  
    user = UserSerializer(read_only=True)  
    class Meta:
        model = BooksBorrowed
        fields = ['book', 'user', 'borrow_date', 'return_date', 'duration_days']




class DailyDueBorrowedSerializer(serializers.Serializer):
    return_date = serializers.DateField()
