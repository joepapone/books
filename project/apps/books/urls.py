from django.urls import path
from apps.books import views


urlpatterns = [
    path('books/', views.BookList.as_view(),name='books'),
    path('book/<int:pk>/', views.BookDetail.as_view(),name='book'),
    path('book/add/', views.BookCreate.as_view(),name='book-add'),
    path('book/update/<int:pk>/', views.BookUpdate.as_view(),name='book-update'),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(),name='book-delete'),

    path('authors/', views.AuthorList.as_view(),name='authors'),
    path('author/<int:pk>/', views.AuthorDetail.as_view(),name='author'),
    path('author/add/', views.AuthorCreate.as_view(),name='author-add'),
    path('author/update/<int:pk>/', views.AuthorUpdate.as_view(),name='author-update'),
    path('author/delete/<int:pk>/', views.AuthorDelete.as_view(),name='author-delete'),
    
    path('publishers/', views.PublisherList.as_view(),name='publishers'),
    path('publisher/<int:pk>/', views.PublisherDetail.as_view(),name='publisher'),
    path('publisher/add/', views.PublisherCreate.as_view(),name='publisher-add'),
    path('publisher/update/<int:pk>/', views.PublisherUpdate.as_view(),name='publisher-update'),
    path('publisher/delete/<int:pk>/', views.PublisherDelete.as_view(),name='publisher-delete'),

    path('genres/', views.GenreList.as_view(),name='genres'),
    path('genre/books/', views.GenreBooks.as_view(),name='genre-books'),
    path('genre/add/', views.GenreCreate.as_view(),name='genre-add'),
    path('genre/update/<int:pk>/', views.GenreUpdate.as_view(),name='genre-update'),
    path('genre/delete/<int:pk>/', views.GenreDelete.as_view(),name='genre-delete'),

    path('sections/', views.SectionList.as_view(),name='sections'),
    path('section/add/', views.SectionCreate.as_view(),name='section-add'),
    path('section/update/<int:pk>/', views.SectionUpdate.as_view(),name='section-update'),
    path('section/delete/<int:pk>/', views.SectionDelete.as_view(),name='section-delete'),

    path('collections/', views.CollectionList.as_view(),name='collections'),
    path('collection/add/', views.CollectionCreate.as_view(),name='collection-add'),
    path('collection/update/<int:pk>/', views.CollectionUpdate.as_view(),name='collection-update'),
    path('collection/delete/<int:pk>/', views.CollectionDelete.as_view(),name='collection-delete'),   
]