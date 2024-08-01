from django.urls import path
from apps.books import views


urlpatterns = [
    path('library/', views.LibraryAllView.as_view(),name='library-all'),
    path('library/favourites', views.LibraryFavoritesView.as_view(),name='library-favorites'),
    path('library/wishlist', views.LibraryWishView.as_view(),name='library-wishlist'),
    path('library/toread', views.LibraryToRead.as_view(),name='library-toread'),
    path('library/loaned', views.LibraryLoaned.as_view(),name='library-loaned'),
    path('library/sold', views.LibrarySold.as_view(),name='library-sold'),

    path('books/', views.BookList.as_view(),name='book-list'),
    path('book/<int:pk>/', views.BookDetail.as_view(),name='book-detail'),
    path('book/add/', views.BookCreate.as_view(),name='book-add'),
    path('book/update/<int:pk>/', views.BookUpdate.as_view(),name='book-update'),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(),name='book-delete'),

    path('authors/', views.AuthorList.as_view(),name='author-list'),
    path('author/<int:pk>/', views.AuthorDetail.as_view(),name='author-detail'),
    path('author/add/', views.AuthorCreate.as_view(),name='author-add'),
    path('author/update/<int:pk>/', views.AuthorUpdate.as_view(),name='author-update'),
    path('author/delete/<int:pk>/', views.AuthorDelete.as_view(),name='author-delete'),
    
    path('publishers/', views.PublisherList.as_view(),name='publisher-list'),
    path('publisher/<int:pk>/', views.PublisherDetail.as_view(),name='publisher'),
    path('publisher/add/', views.PublisherCreate.as_view(),name='publisher-add'),
    path('publisher/update/<int:pk>/', views.PublisherUpdate.as_view(),name='publisher-update'),
    path('publisher/delete/<int:pk>/', views.PublisherDelete.as_view(),name='publisher-delete'),

    path('genres/', views.GenreList.as_view(),name='genre-list'),
    path('genre/books/', views.GenreBooks.as_view(),name='genre-books'),
    path('genre/add/', views.GenreCreate.as_view(),name='genre-add'),
    path('genre/update/<int:pk>/', views.GenreUpdate.as_view(),name='genre-update'),
    path('genre/delete/<int:pk>/', views.GenreDelete.as_view(),name='genre-delete'),

    path('sections/', views.SectionList.as_view(),name='section-list'),
    path('section/add/', views.SectionCreate.as_view(),name='section-add'),
    path('section/update/<int:pk>/', views.SectionUpdate.as_view(),name='section-update'),
    path('section/delete/<int:pk>/', views.SectionDelete.as_view(),name='section-delete'),

    path('collections/', views.CollectionList.as_view(),name='collection-list'),
    path('collection/add/', views.CollectionCreate.as_view(),name='collection-add'),
    path('collection/update/<int:pk>/', views.CollectionUpdate.as_view(),name='collection-update'),
    path('collection/delete/<int:pk>/', views.CollectionDelete.as_view(),name='collection-delete'),   
]