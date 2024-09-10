from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.db import transaction, IntegrityError
from django.db.models import OuterRef, Subquery, IntegerField, CharField, Value, Avg
from django.db.models.functions import Coalesce

# Application modules
from apps.books.models import Book, Author, Publisher, Genre, Section, Collection, Rating, Status, Price
from apps.books.forms import BookForm, AuthorForm, PublisherForm, GenreForm, CollectionForm, SectionForm, PriceForm, RatingForm, StatusForm, BookSelectionForm
from apps.books.custom import star_range

# Application views

# --- Library --- #
class LibraryAllListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=[ 't', 'a', 'r', 'l','f', 'n'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context['title'] = _('My Books')
        return context

class LibraryFavoritesListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with rating >= 3 and status in the specified list
        queryset = queryset.filter(rating__gte=3).order_by('-rating')
        queryset = queryset.filter(status__in=['t', 'a', 'l', 'f'])

        return queryset
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['title'] = _('Favorites')
        context['favorite_count'] = self.get_queryset().count()
        return context

class LibraryWishListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=['w'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        context['title'] = _('Wishlist')
        return context

class LibraryToReadListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=['t'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        context['title'] = _('To Read')
        return context

class LibraryLoanedListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=['l'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        context['title'] = _('Loaned')
        return context

class LibrarySaleListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=['f'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        context['title'] = _('For sale')
        return context   

class LibrarySoldListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/library_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        user = self.request.user

        # Subquery to get the rating for each book for the current user
        rating_subquery = Rating.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('rating')[:1]

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        queryset = Book.objects.annotate(
            rating=Coalesce(Subquery(rating_subquery, output_field=IntegerField()), 0),
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters, books with status in the specified list
        queryset = queryset.filter(status__in=['s'])

        return queryset
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        context['title'] = _('Sold')
        return context


# --- Books --- #
class BookListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'

    def get_queryset(self):
        # Filter according to currently logged-in user
        return Book.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        user = self.request.user

        # Subquery to get the purchase price for this book and the current user
        price_subquery = Price.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).order_by('-created').values('purchase_price')[:1]

        # Subquery to get the current status for this book and the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).order_by('-created').values('status')[:1]

        # Annotate book with price and status
        book = Book.objects.annotate(
            price=Subquery(price_subquery),
            status=Subquery(status_subquery),
        ).get(pk=self.kwargs['pk'])

        return book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        book = context['book']
        
        # Get the current user's rating for this book
        rating = Rating.objects.filter(user=user, book=book).first()

        # Calculate the average rating and number of ratings for the book
        average_rating = book.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        rating_count = book.ratings.count()

        # Get the next URL if provided
        next_url = self.request.GET.get('next', reverse('book_list'))
    
        # Add data to context
        context['book'].rating = rating.rating if rating else None
        context['average_rating'] = round(average_rating, 2)
        context['rating_count'] = rating_count
        context['next_url'] = next_url
        
        return context
 
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    
    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs before it's instantiated
        kwargs['user'] = self.request.user
        return kwargs
      
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The book was updated successfully.'))
        
        return response

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next', '')
        return context

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs before it's instantiated
        kwargs['user'] = self.request.user
        return kwargs
      
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The book was updated successfully.'))
        
        return response
    
    def get_success_url(self):
        # Get the 'next' parameter from the URL's query parameters
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            # Fallback URL in case 'next' is not provided
            return reverse_lazy('book_list')
    
class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('The book was deleted successfully.'))
        return super(BookDeleteView,self).form_valid(form)

class BookRatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm

    def get_object(self, queryset=None):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        rating, created = Rating.objects.get_or_create(book=book, user=self.request.user)
        return rating

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'rating': self.object.rating})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'books/status_form.html'
    
    def get_queryset(self):
        # Ensure that the user can only update their own status records
        return Status.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Save the form and return the HttpResponse
        form.instance.user = self.request.user
    
        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The status was updated successfully.'))
        
        return response

    def get_success_url(self):
        # Redirect to the book's detail view after a successful update
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})

class PriceUpdateView(LoginRequiredMixin, UpdateView):
    model = Price
    form_class = PriceForm
    template_name = 'books/price_form.html'
    
    def get_queryset(self):
        # Ensure that the user can only update their own price records
        return Price.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Save the form and return the HttpResponse
        form.instance.user = self.request.user
    
        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The price was updated successfully.'))
        
        return response

    def get_success_url(self):
        # Redirect to the book's detail view after a successful update
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})


# --- Authors --- #
class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'books/authors_list.html'
    paginate_by = 10

    def get_queryset(self):
        # Restrict object filter to current user
        return Author.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context

class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    context_object_name = 'author'

    def get_queryset(self):
        # Restrict object filter to current user
        return Author.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object).order_by('title')
        return context
    
class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('author_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The author was added successfully.'))
        
        return response
    
class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('author_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The author was updated successfully.'))
        
        return response

class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    context_object_name = 'author'
    success_url = reverse_lazy('author_list')
    
    # This method allows an evaluation before executing the deletion process
    def form_valid(self, form):
        self.object = self.get_object()

        try:
            # Ensure the existence check and deletion happen within a single atomic transaction 
            with transaction.atomic():
                if self.object.book_set.exists():
                    messages.error(self.request, _('The author cannot be deleted because there are books associated with this author.'))
                    return redirect(self.success_url)
                
                response = super().form_valid(form)
                messages.success(self.request, _('The author was deleted successfully.'))
                return response
            
        except IntegrityError:
            # Although form_valid minimizes a RestrictedError, this exception handles errors resulting highly concurrent systems 
            messages.error(self.request, _('An error occurred while trying to delete the author. Please try again.'))
            return redirect(self.success_url)


# --- Publishers --- #
class PublisherListView(LoginRequiredMixin, ListView):
    model = Publisher
    context_object_name = 'publishers'
    template_name = 'books/publishers_list.html'

    def get_queryset(self):
        # Restrict object filter to current user
        return Publisher.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context

class PublisherDetailView(LoginRequiredMixin, DetailView):
    model = Publisher
    context_object_name = 'publisher'

    def get_queryset(self):
        # Restrict object filter to current user
        return Publisher.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(publisher=self.object).order_by('title')
        return context

class PublisherCreateView(LoginRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    success_url = reverse_lazy('publisher_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs before it's instantiated
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The publisher was added successfully.'))
        
        return response

class PublisherUpdateView(LoginRequiredMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    success_url = reverse_lazy('publisher_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The publisher was updated successfully.'))
        
        return response

class PublisherDeleteView(LoginRequiredMixin, DeleteView):
    model = Publisher
    context_object_name = 'publisher'
    success_url = reverse_lazy('publisher_list')
    
    # This method allows an evaluation before executing the deletion process
    def form_valid(self, form):
        self.object = self.get_object()

        try:
            # Ensure the existence check and deletion happen within a single atomic transaction 
            with transaction.atomic():
                if self.object.book_set.exists():
                    messages.error(self.request, _('The publisher cannot be deleted because there are books associated with this publisher.'))
                    return redirect(self.success_url)
                
                response = super().form_valid(form)
                messages.success(self.request, _('The publisher was deleted successfully.'))
                return response
            
        except IntegrityError:
            # Although form_valid minimizes a RestrictedError, this exception handles errors resulting highly concurrent systems 
            messages.error(self.request, _('An error occurred while trying to delete the publisher. Please try again.'))
            return redirect(self.success_url)


# --- Genres --- #
class GenreListView(LoginRequiredMixin, ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'books/genres_list.html'

    def get_queryset(self):
        # Restrict object filter to current user
        return Genre.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context
    
class GenreDetailView(LoginRequiredMixin, DetailView):
    model = Genre
    context_object_name = 'genre'

    def get_queryset(self):
        # Restrict object filter to current user
        return Genre.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(genre=self.object).order_by('title')
        return context 

class GenreBooksView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'genres'
    #queryset = Book.objects.filter(genre='war')[:5]
    template_name = 'books/book_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Book.genre
        return context

class GenreCreateView(LoginRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy('genre_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The genre was added successfully.'))
        
        return response
    
class GenreUpdateView(LoginRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy('genre_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The genre was updated successfully.'))
        
        return response
    
class GenreDeleteView(LoginRequiredMixin, DeleteView):
    model = Genre
    context_object_name = 'genre'
    success_url = reverse_lazy('genre_list')
    
    # This method allows an evaluation before executing the deletion process
    def form_valid(self, form):
        self.object = self.get_object()

        try:
            # Ensure the existence check and deletion happen within a single atomic transaction 
            with transaction.atomic():
                if self.object.book_set.exists():
                    messages.error(self.request, _('The genre cannot be deleted because there are books associated with this genre.'))
                    return redirect(self.success_url)
                
                response = super().form_valid(form)
                messages.success(self.request, _('The genre was deleted successfully.'))
                return response
            
        except IntegrityError:
            # Although form_valid minimizes a RestrictedError, this exception handles errors resulting highly concurrent systems 
            messages.error(self.request, _('An error occurred while trying to delete the genre. Please try again.'))
            return redirect(self.success_url)


# --- Collection --- #
class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    context_object_name = 'collections'
    template_name = 'books/collection_list.html'

    def get_queryset(self):
        # Filter according to currently logged-in user
        return Collection.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context

class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    context_object_name = 'collection'
    template_name = 'books/collection_detail.html'

    def get_queryset(self):
        # Restrict object filter to current user
        return Collection.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        collection = self.get_object()

        # Subquery to get the status for each book for the current user
        status_subquery = Status.objects.filter(
            book=OuterRef('pk'),
            user=user
        ).values('status')[:1]

        # Annotate each book with the user rating and book status
        books_queryset = Book.objects.filter(collection=collection).annotate(
            status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
        )

        # Apply filters to the books queryset
        books_queryset = books_queryset.filter(status__in=['t', 'a', 'l', 'f']).order_by('volume_number')

        # Add the filtered books to the context
        context['books'] = books_queryset
        return context

class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'books/collection_form.html'
    success_url = reverse_lazy('collection_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the collection before saving
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, _('The collection was added successfully.'))

        return response

class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'books/collection_form.html'
    success_url = reverse_lazy('collection_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('The collection was updated successfully.'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(f"Form errors: {form.errors}")  # Debugging
        # You can add additional logging or debugging information here
        return response
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Loaded object: {obj}")
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this collection.")
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        print(f"Form instance: {form.instance}")
        return form

class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    context_object_name = 'collection'
    success_url = reverse_lazy('collection_list')
    
    # This method allows an evaluation before executing the deletion process
    def form_valid(self, form):
        self.object = self.get_object()

        try:
            # Ensure the existence check and deletion happen within a single atomic transaction 
            with transaction.atomic():
                if self.object.book_set.exists():
                    messages.error(self.request, _('The collection cannot be deleted because there are books associated with this collection.'))
                    return redirect(self.success_url)
                
                response = super().form_valid(form)
                messages.success(self.request, _('The collection was deleted successfully.'))
                return response
            
        except IntegrityError:
            # Although form_valid minimizes a RestrictedError, this exception handles errors resulting highly concurrent systems 
            messages.error(self.request, _('An error occurred while trying to delete the collection. Please try again.'))
            return redirect(self.success_url)

class CollectionBookSelectView(LoginRequiredMixin, FormView):
    template_name = 'books/collection_book_selection.html'
    form_class = BookSelectionForm

    def get_collection(self):
        # Retrieve the collection based on primary key from the URL and belong to the current user
        pk = self.kwargs['pk']
        return get_object_or_404(Collection, id=pk, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.get_collection()
        
        # Get all books that are already in this collection and belong to the current user
        context['books_in_collection'] = Book.objects.filter(collection=collection, user=self.request.user)
        context['collection'] = collection
        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('collection_detail', kwargs={'pk': pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the current user to the form
        kwargs['user'] = self.request.user
        return kwargs
           
    def form_valid(self, form):
        # Handle the form submission
        selected_books = form.cleaned_data['books']
        collection = self.get_collection()

        # Add selected books to the collection
        Book.objects.filter(id__in=[book.id for book in selected_books]).update(collection=collection)
        
        # If no books are selected, we should remove all books from the collection
        if not selected_books:
            Book.objects.filter(collection=collection, user=self.request.user).update(collection=None)
        else:
            # Remove books that are no longer in the collection
            Book.objects.filter(collection=collection, user=self.request.user).exclude(id__in=[book.id for book in selected_books]).update(collection=None)

        return super().form_valid(form)


# --- Section --- #
class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    context_object_name = 'sections'
    template_name = 'books/section_list.html'
    
    def get_queryset(self):
        # Restrict object filter to current user
        return Section.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No need to reassign if context has not been modified
        return context

class SectionDetailView(LoginRequiredMixin, DetailView):
    model = Section
    context_object_name = 'section'
    template_name = 'books/section_detail.html'
    
    def get_queryset(self):
        # Restrict object filter to current user
        return Section.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(section=self.object, user=self.request.user).order_by('title')
        return context

class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy('section_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully created
        response = super().form_valid(form)
        messages.success(self.request, ('The section was added successfully.'))
        
        return response

class SectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy('section_list')

    def get_form_kwargs(self):
        # Get the existing form kwargs
        kwargs = super().get_form_kwargs()
        # Add the current user to the form's kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The section was updated successfully.'))

        return response

class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section
    context_object_name = 'section'
    success_url = reverse_lazy('section_list')
    
    # This method allows an evaluation before executing the deletion process
    def form_valid(self, form):
        self.object = self.get_object()

        try:
            # Ensure the existence check and deletion happen within a single atomic transaction 
            with transaction.atomic():
                if self.object.book_set.exists():
                    messages.error(self.request, _('The collection cannot be deleted because there are books associated with this collection.'))
                    return redirect(self.success_url)
                
                response = super().form_valid(form)
                messages.success(self.request, _('The collection was deleted successfully.'))
                return response
            
        except IntegrityError:
            # Although form_valid minimizes a RestrictedError, this exception handles errors resulting highly concurrent systems 
            messages.error(self.request, _('An error occurred while trying to delete the collection. Please try again.'))
            return redirect(self.success_url)

class SectionBookSelectView(LoginRequiredMixin, FormView):
    template_name = 'books/section_book_selection.html'
    form_class = BookSelectionForm

    def get_section(self):
        # Retrieve the section based on primary key from the URL and belong to the current user
        pk = self.kwargs['pk']
        return get_object_or_404(Section, id=pk, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.get_section()
        
        # Get all books that are already in this section and belong to the current user
        context['books_in_section'] = Book.objects.filter(section=section, user=self.request.user)
        context['section'] = section
        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('section_detail', kwargs={'pk': pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the current user to the form
        kwargs['user'] = self.request.user
        return kwargs
           
    def form_valid(self, form):
        # Handle the form submission
        selected_books = form.cleaned_data['books']
        section = self.get_section()

        # Add the selected books to the section
        for book in selected_books:
            book.section = section
            book.save()

        # If no books are selected, we should remove all books from the section
        if not selected_books:
            Book.objects.filter(section=section, user=self.request.user).update(section=None)
        else:
            # Remove books that were previously in the section but are not selected anymore
            books_to_remove = Book.objects.filter(section=section, user=self.request.user).exclude(id__in=[book.id for book in selected_books])
            for book in books_to_remove:
                book.section = None
                book.save()

        return super().form_valid(form)
