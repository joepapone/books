from django.urls import path
from books.views import BookList, BookDetail, BookCreate, BookUpdate, BookDelete, \
     AuthorList, AuthorDetail, AuthorCreate, AuthorUpdate, AuthorDelete, \
     PublisherList, PublisherDetail, PublisherCreate, PublisherUpdate, PublisherDelete

urlpatterns = [
    path('books/', BookList.as_view(),name='books'),
    path('book/<int:pk>/', BookDetail.as_view(),name='book'),
    path('book/create/', BookCreate.as_view(),name='book-create'),
    path('book/update/<int:pk>/', BookUpdate.as_view(),name='book-update'),
    path('book/delete/<int:pk>/', BookDelete.as_view(),name='book-delete'),

    path('authors/', AuthorList.as_view(),name='authors'),
    path('author/<int:pk>/', AuthorDetail.as_view(),name='author'),
    path('author/create/', AuthorCreate.as_view(),name='author-create'),
    path('author/update/<int:pk>/', AuthorUpdate.as_view(),name='author-update'),
    path('author/delete/<int:pk>/', AuthorDelete.as_view(),name='author-delete'),
    path('publishers/', PublisherList.as_view(),name='publishers'),
    path('publisher/<int:pk>/', PublisherDetail.as_view(),name='publisher'),
    path('publisher/create/', PublisherCreate.as_view(),name='publisher-create'),
    path('publisher/update/<int:pk>/', PublisherUpdate.as_view(),name='publisher-update'),
    path('publisher/delete/<int:pk>/', PublisherDelete.as_view(),name='publisher-delete'),
]