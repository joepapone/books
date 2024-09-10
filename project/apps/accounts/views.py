from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

# Application modules
from apps.accounts.models import Profile
from apps.accounts.forms import AccountRegisterForm, ProfileForm

# Applications views
class AccountRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = AccountRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super().form_valid(form)
    
class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class AccountLogoutView(RedirectView): 
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class AccountProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('profile')
   
    def get_object(self, queryset=None):
        # Ensure the view returns the Profile object associated with the logged-in user
        return self.request.user.profile
    
    def form_valid(self, form):
        # Assign the current user to the instance after form validation
        form.instance.user = self.request.user

        # Add a success message after the instance is successfully updated
        response = super().form_valid(form)
        messages.success(self.request, _('The profile was updated successfully.'))
        
        return response
