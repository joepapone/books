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

from accounts.models import Profile
from accounts.forms import AccountRegisterForm, AccountUpdateForm, ProfileUpdateForm


class Account_RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = AccountRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super(Account_RegisterView, self).form_valid(form)
    

class Account_LoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Account_LogoutView(RedirectView): 
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Account_LogoutView, self).get(request, *args, **kwargs)

'''
class DepartmentCreate(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['name','description']
    success_url = reverse_lazy('departments')
    

    def form_valid(self, form):
        messages.success(self.request, "The department was created successfully.")
        return super(DepartmentCreate,self).form_valid(form)
  '''         
               
class Account_Profile(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user_form = AccountUpdateForm(instance=request.user)
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
        
