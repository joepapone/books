from django.urls import path
from apps.books import views


urlpatterns = [
    path('library/', views.LibraryAllListView.as_view(),name='library_all'),
    path('library/favourites', views.LibraryFavoritesListView.as_view(),name='library_favorites'),
    path('library/wishlist', views.LibraryWishListView.as_view(),name='library_wishlist'),
    path('library/toread', views.LibraryToReadListView.as_view(),name='library_toread'),
    path('library/loaned', views.LibraryLoanedListView.as_view(),name='library_loaned'),
    path('library/sale', views.LibrarySaleListView.as_view(),name='library_sale'),
    path('library/sold', views.LibrarySoldListView.as_view(),name='library_sold'),

    path('books/', views.BookListView.as_view(),name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(),name='book_detail'),
    path('book/add/', views.BookCreateView.as_view(),name='book_add'),
    path('book/update/<int:pk>/', views.BookUpdateView.as_view(),name='book_update'),
    path('book/delete/<int:pk>/', views.BookDeleteView.as_view(),name='book_delete'),
    path('book/<int:pk>/price/update/', views.PriceUpdateView.as_view(), name='price_update'),
    path('book/<int:pk>/rate/', views.BookRatingUpdateView.as_view(), name='rating_update'),
    path('book/<int:pk>/status/update/', views.StatusUpdateView.as_view(), name='status_update'),

    path('authors/', views.AuthorListView.as_view(),name='author_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(),name='author_detail'),
    path('author/add/', views.AuthorCreateView.as_view(),name='author_add'),
    path('author/update/<int:pk>/', views.AuthorUpdateView.as_view(),name='author_update'),
    path('author/delete/<int:pk>/', views.AuthorDeleteView.as_view(),name='author_delete'),
    
    path('publishers/', views.PublisherListView.as_view(),name='publisher_list'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(),name='publisher'),
    path('publisher/add/', views.PublisherCreateView.as_view(),name='publisher_add'),
    path('publisher/update/<int:pk>/', views.PublisherUpdateView.as_view(),name='publisher_update'),
    path('publisher/delete/<int:pk>/', views.PublisherDeleteView.as_view(),name='publisher_delete'),

    path('genres/', views.GenreListView.as_view(),name='genre_list'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(),name='genre'),
    path('genre/books/', views.GenreBooksView.as_view(),name='genre_books'),
    path('genre/add/', views.GenreCreateView.as_view(),name='genre_add'),
    path('genre/update/<int:pk>/', views.GenreUpdateView.as_view(),name='genre_update'),
    path('genre/delete/<int:pk>/', views.GenreDeleteView.as_view(),name='genre_delete'),

    path('sections/', views.SectionListView.as_view(),name='section_list'),
    path('section/<int:pk>/', views.SectionDetailView.as_view(),name='section_detail'),
    path('section/add/', views.SectionCreateView.as_view(),name='section_add'),
    path('section/update/<int:pk>/', views.SectionUpdateView.as_view(),name='section_update'),
    path('section/delete/<int:pk>/', views.SectionDeleteView.as_view(),name='section_delete'),
    path('section/<int:pk>/books', views.SectionBookSelectView.as_view(), name='section_book_select'),

    path('collections/', views.CollectionListView.as_view(),name='collection_list'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(),name='collection_detail'),
    path('collection/add/', views.CollectionCreateView.as_view(),name='collection_add'),
    path('collection/update/<int:pk>/', views.CollectionUpdateView.as_view(),name='collection_update'),
    path('collection/delete/<int:pk>/', views.CollectionDeleteView.as_view(),name='collection_delete'),
    path('collection/<int:pk>/books', views.CollectionBookSelectView.as_view(), name='collection_book_select'),
]