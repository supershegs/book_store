from django.contrib import admin

# Register your models here.


from .models import (
    CustomUser,
    Publisher, 
    Category,
)

admin.site.register(CustomUser)
admin.site.register(Publisher)
admin.site.register(Category)
