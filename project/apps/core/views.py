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
    return render(request, 'core/index.html', {'description': "Hi there welcome to our site"})

def home(request):
    """
    Shows the homepage with a welcome message that is translated in the
    user's language.
    """
    message = gettext("Welcome to our site!")

    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    #num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'message': message,
        'num_books': num_books,
        #'num_instances': num_instances,
        #'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    
    return render(request, "core/home.html", context=context)

def about(request):
    return render(request, 'core/about.html', {'description': ABOUT_TEXT})

