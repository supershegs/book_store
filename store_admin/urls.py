from django.urls import path

from .views import (
    AddBookView,
    RemoveBookView,
    AllBorrowedBooksView,
    ListUsersView,
    ListsofDueBooksView,
    DailyDueBorrowed
)
urlpatterns = [
    path('book/add', AddBookView.as_view()),
    path('book/remove-book/<int:book_id>/', RemoveBookView.as_view(), name='remove-book'),
    path('book/List-borrowed-books', AllBorrowedBooksView.as_view()),
    path('list-users/', ListUsersView.as_view(), name='list-users'),
    # path('user-borrowed-books/', UserBorrowedBooksView.as_view(), name='user-borrowed-books'),
    path('book/list-of-due-borrowed-books/', ListsofDueBooksView.as_view(), name='unavailable-books'),
    path('book/list-of-daily-due-borrowed-books/', DailyDueBorrowed.as_view(), name='list-due-borrowed')
]