from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden
from django import forms
from django.views import View
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.db.models import Q
from apps.books.models import Book, Author, Publisher, Genre, Section, Collection, Rating, Status
from apps.books.forms import RatingForm


# --- Library --- #
class LibraryListAllView(ListView):
    template_name = 'books/library_list.html'
    model = Book
    context_object_name = 'object_list'
    
    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('status').filter(Q(status__status='a') | Q(status__status='t')).order_by('title')
        context['title'] = 'My Books'
        return context
    

class LibraryListFavoritesView(ListView):
    template_name = 'books/library_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('rating').filter(rating__rating__gte=3).order_by('-rating__rating')
        context['title'] = 'Favorites'
        return context


class LibraryListWishView(ListView):
    template_name = 'books/library_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('status').filter(status__status='w').order_by('title')
        context['title'] = 'Wishlist'
        return context


class LibraryListToReadView(ListView):
    template_name = 'books/library_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('status').filter(status__status='t').order_by('title')
        context['title'] = 'To Read'
        return context


class LibraryListLoanedView(ListView):
    template_name = 'books/library_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('status').filter(status__status='l').order_by('title')
        context['title'] = 'Loaned'
        return context


class LibraryListSoldView(ListView):
    template_name = 'books/library_list.html'
    model = Book

    def get_context_data(self, **kwargs):
        # Base context implementation 
        context = super().get_context_data(**kwargs)
        # Context update
        context["object_list"] = Book.objects.select_related('status').filter(status__status='s').order_by('title')
        context['title'] = 'Sold'
        return context


# --- Books --- #
class BookList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    model = Book
    context_object_name = 'books'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = context['books']
        return context


class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['isbn','title', 'author', 'copyright', 'publisher', 'edition', 'category', 'genre', 'language', 'comments' ]
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']

        # Create record with default values
        book_rating = Rating(rating=0, created_by=self.request.user)
        book_rating.save()
        form.instance.rating = book_rating

        # Create record with default values
        book_status = Status(status=0, created_by=self.request.user)
        book_status.save()
        form.instance.status = book_status

        messages.success(self.request, "The book was added successfully.")
        return super(BookCreate,self).form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['isbn','title', 'author', 'copyright', 'publisher', 'edition', 'category', 'genre', 'language', 'comments']
    success_url = reverse_lazy('book-list')
        
    def form_valid(self, form):       
        form.instance.created_by = self.request.user
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']
        
        messages.success(self.request, "The book was updated successfully.")
        return super(BookUpdate,self).form_valid(form)


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('book-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The book was deleted successfully.")
        return super(BookDelete,self).form_valid(form)


class BookRating(FormView):
    template_name = 'books/rating.html'

    def post(self, request, *args, **kwargs):
        # Proceed only if authenticated user
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # Extract redirect path
        path= request.POST.get('next')
        
        if request.method == "POST":
            # Create a form instance and populate it with data from POST request
            form = RatingForm(request.POST)
            # Check if form data has been validated
            if form.is_valid():
                # Extract cleaned data to load to database
                dict = form.cleaned_data
                rating = dict['stars']
                book_id = dict['id']
                rating_id = Book.objects.get(id=book_id).status_id

                # Update changes to database
                Rating.objects.filter(id=rating_id).update(rating=rating, created_by=self.request.user)
        
        return  redirect(path)


# --- Authors --- #
class AuthorList(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = 'authors'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = context['authors']
        return context


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object).order_by('title')
        return context


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death','summary']
    success_url = reverse_lazy('author-list')  

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if 'headshot' in self.request.FILES:
            form.instance.headshot = self.request.FILES['headshot']
        
        messages.success(self.request, "The author was added successfully.")
        return super(AuthorCreate,self).form_valid(form)


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death','summary']
    success_url = reverse_lazy('author-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user        
        if 'headshot' in self.request.FILES:
            form.instance.headshot = self.request.FILES['headshot']
        
        messages.success(self.request, "The author was updated successfully.")
        return super(AuthorUpdate,self).form_valid(form)


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    context_object_name = 'author'
    success_url = reverse_lazy('author-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The author was deleted successfully.")
        return super(AuthorDelete,self).form_valid(form)


# --- Publishers --- #
class PublisherList(LoginRequiredMixin, ListView):
    model = Publisher
    context_object_name = 'publishers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publishers'] = context['publishers']
        return context


class PublisherDetail(LoginRequiredMixin, DetailView):
    model = Publisher
    context_object_name = 'publisher'


class PublisherCreate(LoginRequiredMixin, CreateView):
    model = Publisher
    fields = ['name','description']
    success_url = reverse_lazy('publisher-list')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The publisher was added successfully.")
        return super(PublisherCreate,self).form_valid(form)


class PublisherUpdate(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ['name','description']
    success_url = reverse_lazy('publisher-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The publisher was updated successfully.")
        return super(PublisherUpdate,self).form_valid(form)


class PublisherDelete(LoginRequiredMixin, DeleteView):
    model = Publisher
    context_object_name = 'publisher'
    success_url = reverse_lazy('publisher-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The publisher was deleted successfully.")
        return super(PublisherDelete,self).form_valid(form)


# --- Genres --- #
class GenreList(LoginRequiredMixin, ListView):
    model = Genre
    context_object_name = 'genres'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = context['genres']
        return context


class GenreBooks(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'genres'
    #queryset = Book.objects.filter(genre='war')[:5]
    template_name = 'books/book_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Book.genre
        return context


class GenreCreate(LoginRequiredMixin, CreateView):
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genre-list')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The genre was added successfully.")
        return super(GenreCreate,self).form_valid(form)


class GenreUpdate(LoginRequiredMixin, UpdateView):
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genre-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The genre was updated successfully.")
        return super(GenreUpdate,self).form_valid(form)


class GenreDelete(LoginRequiredMixin, DeleteView):
    model = Genre
    context_object_name = 'genre'
    success_url = reverse_lazy('genre-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The genre was deleted successfully.")
        return super(GenreDelete,self).form_valid(form)


# --- Section --- #
class SectionList(LoginRequiredMixin, ListView):
    model = Section
    context_object_name = 'sections'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = context['sections']
        return context


class SectionCreate(LoginRequiredMixin, CreateView):
    model = Section
    fields = ['name']
    success_url = reverse_lazy('section-list')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The section was added successfully.")
        return super(SectionCreate,self).form_valid(form)


class SectionUpdate(LoginRequiredMixin, UpdateView):
    model = Section
    fields = ['name']
    success_url = reverse_lazy('section-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The section was updated successfully.")
        return super(SectionUpdate,self).form_valid(form)


class SectionDelete(LoginRequiredMixin, DeleteView):
    model = Section
    context_object_name = 'section'
    success_url = reverse_lazy('section-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The section was deleted successfully.")
        return super(SectionDelete,self).form_valid(form)


# --- Collection --- #
class CollectionList(LoginRequiredMixin, ListView):
    model = Collection
    context_object_name = 'collections'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = context['collections']
        return context


class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['name','description']
    success_url = reverse_lazy('collection-list')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The collection was added successfully.")
        return super(CollectionCreate,self).form_valid(form)


class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = ['name','description']
    success_url = reverse_lazy('collection-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The collection was updated successfully.")
        return super(CollectionUpdate,self).form_valid(form)


class CollectionDelete(LoginRequiredMixin, DeleteView):
    model = Collection
    context_object_name = 'collection'
    success_url = reverse_lazy('collection-list')
    
    def form_valid(self, form):
        messages.success(self.request, "The collection was deleted successfully.")
        return super(CollectionDelete,self).form_valid(form)




    '''

        # Create record with default values
        obj, created = Rating.objects.update_or_create(
            rating=form.instance.id,
            create_defaults={'rating': 0 , 'created_by': self.request.user,})
        

        # Create record with default values
        obj, created = Status.objects.update_or_create(
            book_id=form.instance.id,
            create_defaults={'book_id': form.instance.id, 'status': 'a', 'created_by': self.request.user,})


class LibraryAllView(View):  
    def get(self, request, *args, **kwargs):
        view = LibraryListAll.as_view()
        return view(request, *args, **kwargs)



class LibraryBookRating(SingleObjectMixin, FormView):
    form_class = RatingForm1
    model = Rating
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        rating = request.POST.get('stars')
        book_id= request.POST.get('id')
        created_by = self.request.user
        
        # Use defaults for updating and create_defaults for creating new record
        obj, created = Rating.objects.update_or_create(
            book_id=book_id,
            defaults={'book_id': book_id, 'rating': rating, 'created_by': created_by,},
            create_defaults={'book_id': book_id, 'rating': rating, 'created_by': created_by,},
            )

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        # Define redirect according to request path
        viewname='library-all'
        if self.request.path == '/library/favourites':
            viewname = 'library-favorites'

        return reverse(viewname)


    def upload_file(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('books')
        else:
            form = UploadFileForm()
        return render(request, 'upload_form.html', {'form': form})


    def upload_file(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('books')
        else:
            form = UploadFileForm()
        return render(request, 'upload_form.html', {'form': form})


    from . models import UploadedFile

    def upload_file1(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                instance = UploadedFile(file=request.FILES["file"])
                instance.save()
                return redirect('books')
        else:
            form = UploadFileForm()
        return render(request, "upload_form.html", {"form": form})

    def upload_file2(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                instance = UploadedFile(file=request.FILES["file"])
                instance.save()
                return redirect('books')
        else:
            form = UploadFileForm()
        return render(request, "upload_form.html", {"form": form})


    from django.shortcuts import render

    def upload_file3(request):
        if request.method == 'POST':
            print(request)
            #uploaded_file = request.FILES['file']
            # process the uploaded file here
            return render(request, 'upload-file.html', {'message': 'File uploaded successfully'})
        else:
            return render(request, 'upload-file.html')
        

    from django.conf import settings
    from pathlib import Path
    from django.core.files.storage import default_storage

    def file_upload(request):
        save_path = Path(settings.MEDIA_ROOT, 'uploads', request.FILES['file'])
        print(f'Path: {save_path}')
        path = default_storage.save(save_path, request.FILES['file'])
        return default_storage.path(path)



    '''

    
    '''

    def post(self, request, *args, **kwargs):
    print(f"Post 1 {request.POST}")

    return HttpResponseRedirect("/books/")
    profile_form = ProfileForm(data=request.POST)
    if profile_form.is_valid():
        if 'picture' in request.FILES:
            current_user.image = request.FILES['image']
    '''

    '''
    form_class = BookForm
    #initial = {"key": "value"}
    #initial = {"title": "testing #1"}
    #user_form = AccountUpdateForm(instance=request.user)
    template_name = "books/book_form.html"

    def get(self, request, *args, **kwargs):
        #form = self.form_class(initial=self.initial)
        #initial = Book(instance=request.GET)

        form = self.form_class()

        print(f"testform {request.GET}")
        
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Your profile has been updated successfully")
            # <process form cleaned data>
            return HttpResponseRedirect("/books/")
        else:
            messages.error(request,"Error updating you profile")

            return render(request, self.template_name, {"form": form})
    
    '''

    '''
    class Account_Profile(LoginRequiredMixin, View):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'

        def get(self, request):
            user_form = AccountUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.profile)
        
            context = {
                'user_form': user_form,
                #'profile_form': profile_form
            }
            
            return render(request, 'accounts/profile.html', context)
        
        def post(self,request):
            user_form = AccountUpdateForm(
                request.POST, 
                instance=request.user
            )
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user.profile
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                
                messages.success(request,'Your profile has been updated successfully')
                
                return redirect('profile')
            else:
                context = {
                    'account_form': user_form,
                    'profile_form': profile_form
                }
                messages.error(request,'Error updating you profile')
                
                return render(request, 'accounts/profile.html', context)
        
    '''
