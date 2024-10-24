from django.db import models
from django.utils import timezone
from common.models import (
    Publisher,
    Category,
    CustomUser)
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='user_books')
    categories = models.ManyToManyField(Category, related_name='user_books')
    published_date = models.DateField()
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_borrowed_books')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_borrowed_books')  # Use CustomUser
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} for {self.duration_days} days"

    
    @property
    def due_days(self):
        today_date = timezone.now().date()
        return (self.return_date - today_date).days