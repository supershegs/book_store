from django.contrib import admin

# Register your models here.

from .models import (
    BookStore,
    BooksBorrowed
)


admin.site.register(BookStore)
admin.site.register(BooksBorrowed)