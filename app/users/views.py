from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Profile
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views import View


class User_RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super(User_RegisterView, self).form_valid(form)
    

class User_LoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class User_LogoutView(RedirectView): 
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(User_LogoutView, self).get(request, *args, **kwargs)

'''
class DepartmentCreate(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['name','description']
    success_url = reverse_lazy('departments')
    

    def form_valid(self, form):
        messages.success(self.request, "The department was created successfully.")
        return super(DepartmentCreate,self).form_valid(form)
  '''         
               
class User_Profile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        

        #obj, created = Profile.objects.get_or_create(user_id=request.user.id)
        

        '''
        try:
            obj = Profile()
            #profile_form = ProfileUpdateForm(instance=request.user.profile)
            #obj = Person.objects.get(first_name="John", last_name="Lennon")
        except Profile.DoesNotExist:
            obj = Person(first_name="John", last_name="Lennon", birthday=date(1940, 10, 9))
            profile_form.save()
        '''

        context = {
            'user_form': user_form,
            #'profile_form': profile_form
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self,request):
        user_form = UserUpdateForm(
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
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating you profile')
            
            return render(request, 'users/profile.html', context)