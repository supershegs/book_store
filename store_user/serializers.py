from rest_framework import serializers



from .models import (
    Book,
    BorrowedBook,
    CustomUser
)

from common.serializers import (
    PublisherSerializer,
    CategorySerializer
)

class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'categories', 'published_date', 'available_copies']
        
        

class BorrowedBookSerializer(serializers.ModelSerializer):
    return_date = serializers.SerializerMethodField()
    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'user', 'borrow_date', 'return_date', 'duration_days']

    def get_return_date(self, obj):
        return obj.return_date
        # return obj.return_date.date() 
    
    
class BookBorrowSerializer(serializers.Serializer):
    duration_days = serializers.IntegerField()
    
    def validate_duration_days(self, value):
        if value > 5:
            raise serializers.ValidationError("The duration must not exceed 5 working days.")
        if value <= 0:
            raise serializers.ValidationError("The duration must be a positive number.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']
        
        
        
        

class ListBorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  
    user = UserSerializer(read_only=True)  
    class Meta:
        model = BorrowedBook
        fields = ['book', 'user', 'borrow_date', 'return_date', 'duration_days']
