from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from apps.books.models import Book, Author, Publisher, Genre, Section, Collection


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
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']

        messages.success(self.request, "The book was added successfully.")
        return super(BookCreate,self).form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['isbn','title', 'author', 'copyright', 'publisher', 'edition', 'category', 'genre', 'language', 'comments']
    success_url = reverse_lazy('books')
        
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']

        messages.success(self.request, "The book was updated successfully.")
        return super(BookUpdate,self).form_valid(form)


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('books')
    
    def form_valid(self, form):
        messages.success(self.request, "The book was deleted successfully.")
        return super(BookDelete,self).form_valid(form)


# --- Authors --- #
class AuthorList(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = 'authors'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = context['authors']
        return context


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    context_object_name = 'author'


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death','summary']
    success_url = reverse_lazy('authors')  

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if 'headshot' in self.request.FILES:
            form.instance.headshot = self.request.FILES['headshot']
        
        messages.success(self.request, "The author was added successfully.")
        return super(AuthorCreate,self).form_valid(form)


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death','summary']
    success_url = reverse_lazy('authors')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user        
        if 'headshot' in self.request.FILES:
            form.instance.headshot = self.request.FILES['headshot']
        
        messages.success(self.request, "The author was updated successfully.")
        return super(AuthorUpdate,self).form_valid(form)


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    context_object_name = 'author'
    success_url = reverse_lazy('authors')
    
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
    success_url = reverse_lazy('publishers')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The publisher was added successfully.")
        return super(PublisherCreate,self).form_valid(form)


class PublisherUpdate(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ['name','description']
    success_url = reverse_lazy('publishers')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The publisher was updated successfully.")
        return super(PublisherUpdate,self).form_valid(form)


class PublisherDelete(LoginRequiredMixin, DeleteView):
    model = Publisher
    context_object_name = 'publisher'
    success_url = reverse_lazy('publishers')
    
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
    success_url = reverse_lazy('genres')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The genre was added successfully.")
        return super(GenreCreate,self).form_valid(form)


class GenreUpdate(LoginRequiredMixin, UpdateView):
    model = Genre
    fields = ['name']
    success_url = reverse_lazy('genres')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The genre was updated successfully.")
        return super(GenreUpdate,self).form_valid(form)


class GenreDelete(LoginRequiredMixin, DeleteView):
    model = Genre
    context_object_name = 'genre'
    success_url = reverse_lazy('genres')
    
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
    success_url = reverse_lazy('sections')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The section was added successfully.")
        return super(SectionCreate,self).form_valid(form)


class SectionUpdate(LoginRequiredMixin, UpdateView):
    model = Section
    fields = ['name']
    success_url = reverse_lazy('sections')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The section was updated successfully.")
        return super(SectionUpdate,self).form_valid(form)


class SectionDelete(LoginRequiredMixin, DeleteView):
    model = Section
    context_object_name = 'section'
    success_url = reverse_lazy('sections')
    
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
    success_url = reverse_lazy('collections')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The collection was added successfully.")
        return super(CollectionCreate,self).form_valid(form)


class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = ['name','description']
    success_url = reverse_lazy('collections')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "The collection was updated successfully.")
        return super(CollectionUpdate,self).form_valid(form)


class CollectionDelete(LoginRequiredMixin, DeleteView):
    model = Collection
    context_object_name = 'collection'
    success_url = reverse_lazy('collections')
    
    def form_valid(self, form):
        messages.success(self.request, "The collection was deleted successfully.")
        return super(CollectionDelete,self).form_valid(form)




    '''
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
