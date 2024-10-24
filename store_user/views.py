# from time import timezone
from datetime import timedelta

from django.utils import timezone  
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    Book,  
    BorrowedBook
)

from common.utils import (
    SuccessApiResponse,
    FailureApiResponse,
    ServerErrorApiResponse
)
from .serializers import (
    BookSerializer, 
    BookBorrowSerializer, 
    BorrowedBookSerializer,
    ListBorrowedBookSerializer
)

from store_admin.models import (
    BooksBorrowed,
    BookStore,
    TemporaryBorrowedList
)

class AvailableBooksView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            books = Book.objects.filter(available_copies__gt=0)
            serializer = BookSerializer(books, many=True)
            # if serializer.data == [] or None:
            #     return FailureApiResponse( "list of available book is empty", serializer.data)
            return SuccessApiResponse( "list fetched",serializer.data)    
        except Exception as e:
            return ServerErrorApiResponse("failed to fetch", str(e))
            
class BookDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, book_id):
        try:
            book = get_object_or_404(Book, pk=book_id)
            serializer = BookSerializer(book)
            return SuccessApiResponse( "book fetched",serializer.data)
        except Exception as e:
            return FailureApiResponse("failed to fetch", str(e))
            


class FilterBooksPublisherView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            publisher_name = request.query_params.get('publisher')
            books = Book.objects.all()
            if publisher_name:
                books = books.filter(publisher__name__iexact=publisher_name)
                serializer = BookSerializer(books, many=True)
                return SuccessApiResponse( "books fetched by publisher name",serializer.data)
            return FailureApiResponse('add pushisher name to the params')
        except Exception as e:
            return FailureApiResponse("failed to fetch", str(e))
        

class FilterBooksCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            category_name = request.query_params.get('category')
            books = Book.objects.all()
            if category_name:
                books = books.filter(categories__name__iexact=category_name)  
                serializer = BookSerializer(books, many=True)
                return SuccessApiResponse( "books fetched by categories",serializer.data)
            return FailureApiResponse('add category name to the params')
        except Exception as e:
            return FailureApiResponse("failed to fetch", str(e))

class BorrowBookView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, book_id):
        try:
            book = get_object_or_404(Book, pk=book_id) 
            book_admin = get_object_or_404(BookStore, title=book.title)
                
            if book.available_copies <= 0 and book_admin.available_copies <=0:
                return FailureApiResponse("This book is not available for borrowing", status=status.HTTP_400_BAD_REQUEST)
            
            serializer = BookBorrowSerializer(data=request.data)
            if serializer.is_valid():
                duration_days = serializer.validated_data['duration_days']
                borrowed_books = BorrowedBook.objects.filter(user=request.user)
                for borrowed in borrowed_books:
                    if borrowed.due_days <= 0:
                        return FailureApiResponse(f'Failed to borrow book due to expired due return date, returned date was: {borrowed.return_date}')
                
                
                borrowed_book = BorrowedBook.objects.create(
                    book=book,
                    user=request.user,
                    duration_days=duration_days,
                    return_date=timezone.now() + timedelta(days=duration_days)
                )
                book.available_copies -= 1
                book.save()
                
                borrowed_book_admin = BooksBorrowed.objects.create(
                    book=book_admin,
                    user=request.user,
                    duration_days=duration_days,
                    return_date=timezone.now() + timedelta(days=duration_days)                  
                )
                book_admin.available_copies -= 1
                book_admin.save()
                
                borrowed_book_serializer = BorrowedBookSerializer(borrowed_book)                
                return SuccessApiResponse( "Book borrowed successfully!", borrowed_book_serializer.data)
            return FailureApiResponse("failed to fetch", serializer.errors)
        except Exception as e:
            return FailureApiResponse("failed to fetch", str(e))
            
            
class UserBorrowedBooksView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        borrowed_books = BorrowedBook.objects.filter(user=request.user)
        print(borrowed_books)
        if not borrowed_books.exists():
            return Response({'message': 'No borrowed books found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListBorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TemporaryReturnBorrowedBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, book_id):
        try:
            borrowed_book = get_object_or_404(BorrowedBook, pk=book_id, user=request.user)
            # import pdb
            # pdb.set_trace()
            TemporaryBorrowedList.objects.create(
                user=request.user,
                borrowed_book=borrowed_book,
                saved_at=timezone.now()  
            )
            serializer = BorrowedBookSerializer(borrowed_book)
            return SuccessApiResponse("Borrowed book details fetched successfully", serializer.data)
        except Exception as e:
            return FailureApiResponse('Failed to get borrowed book', str(e))        

class ReturnBorrowedBooks(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,book_id):
        try:
            book = get_object_or_404(Book, pk=book_id)
            borrowed_book = get_object_or_404(BorrowedBook, user=request.user, book=book)

            serializer = BorrowedBookSerializer(borrowed_book)
            
            return SuccessApiResponse("Borrowed book details fetched successfully", serializer.data)
        except Exception as e:
            return FailureApiResponse('Failed to get borrowed book', str(e))