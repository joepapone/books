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

from apps.books.models import Book, Author, Publisher


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
    fields = ['isbn','title', 'copyright', 'publisher', 'edition']
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        messages.success(self.request, "The book was created successfully.")
        return super(BookCreate,self).form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['isbn','title', 'copyright', 'publisher', 'edition']
    success_url = reverse_lazy('books')
    
    def form_valid(self, form):
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
    fields = ['name','description']
    success_url = reverse_lazy('authors')
    

    def form_valid(self, form):
        messages.success(self.request, "The author was created successfully.")
        return super(AuthorCreate,self).form_valid(form)


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['name','description']
    success_url = reverse_lazy('authors')
    
    def form_valid(self, form):
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
        messages.success(self.request, "The publisher was created successfully.")
        return super(PublisherCreate,self).form_valid(form)


class PublisherUpdate(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ['name','description']
    success_url = reverse_lazy('publishers')
    
    def form_valid(self, form):
        messages.success(self.request, "The publisher was updated successfully.")
        return super(PublisherUpdate,self).form_valid(form)


class PublisherDelete(LoginRequiredMixin, DeleteView):
    model = Publisher
    context_object_name = 'publisher'
    success_url = reverse_lazy('publishers')
    
    def form_valid(self, form):
        messages.success(self.request, "The publisher was deleted successfully.")
        return super(PublisherDelete,self).form_valid(form)

