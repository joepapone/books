from django.contrib import admin
from apps.books.models import Book, Author, Publisher

# Register model to Django Admin app
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
