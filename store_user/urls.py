from django.urls import path

from .views import (
    AvailableBooksView,
    BookDetailView,
    FilterBooksPublisherView,
    FilterBooksCategoryView,
    BorrowBookView,
    UserBorrowedBooksView,
    ReturnBorrowedBooks,
    TemporaryReturnBorrowedBooks
)

urlpatterns = [
    
    path('books/available/', AvailableBooksView.as_view(), name='available-books'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/filter/publisher/', FilterBooksPublisherView.as_view(), name='filter-books'),
    path('books/filter/category/', FilterBooksCategoryView.as_view(), name='filter-books-by-category'),
    path('books/<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('books/List-borrowed-book/', UserBorrowedBooksView.as_view(), name='List-borrowed-books'),
    path('books/borrowed-book/<int:book_id>/', TemporaryReturnBorrowedBooks.as_view(), name='borrowed-book' )
]