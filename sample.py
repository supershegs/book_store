# serializers.py
from rest_framework import serializers
from .models import Book, BorrowedBook
from django.contrib.auth import get_user_model


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'user', 'borrowed_at', 'return_date']


class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True, source='borrowedbook_set')

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'borrowed_books']


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Book, BorrowedBook
from django.contrib.auth import get_user_model
from .serializers import BookSerializer, UserSerializer, BorrowedBookSerializer

User = get_user_model()

class AddBookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveBookView(APIView):
    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response({"message": "Book removed successfully"}, status=status.HTTP_204_NO_CONTENT)


class ListUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserBorrowedBooksView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_borrowed_books = [
            {"user": user.username, "borrowed_books": BorrowedBookSerializer(user.borrowedbook_set.all(), many=True).data}
            for user in users
        ]
        return Response(user_borrowed_books, status=status.HTTP_200_OK)


class UnavailableBooksView(APIView):
    def get(self, request):
        
        borrowed_books = BorrowedBook.objects.filter(return_date__gt=timezone.now())
        unavailable_books = [
            {
                "book_title": borrowed.book.title,
                "borrowed_by": borrowed.user.username,
                "will_be_available_on": borrowed.return_date,
            }
            for borrowed in borrowed_books
        ]
        return Response(unavailable_books, status=status.HTTP_200_OK)
    
    
    


from django.contrib.auth import get_user_model


from .serializers import (
    BookStoreSerializer,
    BooksBorrowedSerializer,
    UserSerializer
)


from common.models import (
    Publisher,
    Category
)

from store_user.models import Book
User = get_user_model()


 