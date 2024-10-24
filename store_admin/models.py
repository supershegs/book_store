from django.db import models
from django.utils import timezone
from common.models import (
    Publisher,
    Category,
    CustomUser)
# Create your models here.

from store_user.models import BorrowedBook

class BookStore(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='admin_books')
    categories = models.ManyToManyField(Category, related_name='admin_books')
    published_date = models.DateField()
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class BooksBorrowed(models.Model):
    book = models.ForeignKey(BookStore, on_delete=models.CASCADE, related_name='admin_borrowed_books')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_borrowed_books')  # Use CustomUser
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} for {self.duration_days} days"

    @property
    def due_days(self):
        today_date = timezone.now().date()
        return (self.return_date - today_date).days
    

class TemporaryBorrowedList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='temporary_borrowed_books')
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE, related_name='temporary_borrowed')
    saved_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.borrowed_book.book.title}"