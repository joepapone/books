from django.shortcuts import render

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


A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 



A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. A web based ERP system for best performance and reliability. 
Designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
'''

def index(request):
    return render(request, 'home/index.html', {'description': "Hi there welcome to our site"})

def home(request):
    return render(request, 'home/home.html', {'description': "Hura you have logged into our site!"})

def about(request):
    return render(request, 'home/about.html', {'description': ABOUT_TEXT})
