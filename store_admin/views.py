from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from common.utils import (
    SuccessApiResponse,
    FailureApiResponse
)
from .models import (
    BookStore,
    BooksBorrowed
)

from django.contrib.auth import get_user_model


from .serializers import (
    BookStoreSerializer,
    BooksBorrowedSerializer,
    UserSerializer,
    ListBorrowedBookSerializer,
    DailyDueBorrowedSerializer
)


from common.models import (
    Publisher,
    Category
)

from store_user.models import (
    Book,
    BorrowedBook
)



User = get_user_model()


class AddBookView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        serializer = BookStoreSerializer(data=request.data)
        if serializer.is_valid():
            
            publisher_name = request.data.get('publisher')
            categories_name = request.data.get('categories')
            
            if isinstance(categories_name, str):
                categories_name = [categories_name]              
            print(categories_name)
            category_objects = []
            for category_name in categories_name:
                category, created_category = Category.objects.get_or_create(
                    name__iexact=category_name, defaults={'name': category_name}
                )
                category_objects.append(category)
            publisher, created_publisher = Publisher.objects.get_or_create(name__iexact=publisher_name, defaults={'name': publisher_name})

            book_store = serializer.save(publisher=publisher) 
            book_store.categories.add(*category_objects)
              
            book = Book.objects.create(
                title=request.data.get('title'),
                author=request.data.get('author'),
                publisher=publisher,
                published_date = request.data.get('published_date'),
                available_copies=request.data.get('available_copies', 1) 
            )
            book.categories.add(*category_objects) 
            
            return SuccessApiResponse("New books added", serializer.data)
        return FailureApiResponse('Failed to add book', serializer.errors)
    
    
class RemoveBookView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, book_id):
        try:
            book_admin = get_object_or_404(BookStore, pk=book_id)
            book_user = Book.objects.filter(title = book_admin.title)
            
            book_admin.delete()
            if book_user.exists():
                print("Book found in user models(DB)")
                book_user.delete()
            return SuccessApiResponse("Book removed successfully", '')
        except Exception as e:
            return FailureApiResponse("failed to delete", str(e))
        
        
class ListUsersView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        users = User.objects.filter(role='user')
        if not users.exists():
            return SuccessApiResponse("No admin users found", [])
        serializer = UserSerializer(users, many=True)
        return SuccessApiResponse("list of user successfully fetched", serializer.data)


class AllBorrowedBooksView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.user.role == 'admin':
            return FailureApiResponse("Access denied: Admins only")                
        borrowed_books = BooksBorrowed.objects.all()
        if not borrowed_books.exists():
            return FailureApiResponse("No borrowed books found.")    
        serializer = ListBorrowedBookSerializer(borrowed_books, many=True)
        return SuccessApiResponse("All borrowed books fetched", serializer.data)
        
 
 
class ListsofDueBooksView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            borrowed_books = BooksBorrowed.objects.all()
            list_of_due_borrowed_book = [
                    {
                        "book_title": borrowed.book.title,
                        "borrowed_by": borrowed.user.username,
                        "borrowed_date":borrowed.borrow_date,
                        "expected_returned_date": borrowed.return_date,
                        'due_days_no': borrowed.due_days
                    }
                    for borrowed in borrowed_books
                ]
            return SuccessApiResponse("List of due borrowed books", list_of_due_borrowed_book)
        except Exception as e:
            return FailureApiResponse('Failed to return List of due borrowed books', str(e))
    

class DailyDueBorrowed(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = DailyDueBorrowedSerializer(data=request.data)
        if serializer.is_valid():
            date = request.data.get('return_date')
            try: 
                borrowed_books = BooksBorrowed.objects.filter(return_date=date)
                due_borrowed_book = [
                    {
                        "book_title": borrowed.book.title,
                        "borrowed_by": borrowed.user.username,
                        "borrowed_date":borrowed.borrow_date,
                        "expected_returned_date": borrowed.return_date,
                        'due_days_no': borrowed.due_days
                    }
                    for borrowed in borrowed_books
                ]
                return SuccessApiResponse(f"All Books to be return today data: {date}", due_borrowed_book)  
            except Exception as e:
                return FailureApiResponse('Failed to return List of  daily due borrowed books', str(e))
    
        return FailureApiResponse('Failed', serializer.errors)
      