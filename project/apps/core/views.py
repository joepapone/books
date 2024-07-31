from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.translation import gettext
from apps.books.models import Book, Author, Publisher


ABOUT_TEXT = '''
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 

A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 

A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
'''

def index(request):
    return render(request, 'core/index.html', {'description': gettext("Hi there welcome to our site")})


class HomeView(TemplateView):
    """
    Shows the homepage with a welcome message that is translated in the
    user's language.
    """
        
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = gettext("Welcome to our site!")
        context['num_books'] = Book.objects.all().count()
        context['num_authors'] = Author.objects.count()
        return context
    
    
class AboutView(TemplateView):     
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = ABOUT_TEXT
        return context
    

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World!")

