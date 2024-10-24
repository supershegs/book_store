from django.contrib import admin

# Register your models here.

from .models import (
    Book,
    BorrowedBook
)

admin.site.register(Book)
admin.site.register(BorrowedBook)