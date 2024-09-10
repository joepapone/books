from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Application modules
from apps.accounts.models import Profile

# Application forms
class AccountRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2', )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Although built-in enforce username uniqueness
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username is already taken.")
        
        return username

class ProfileForm(forms.ModelForm):   
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('First name ...')})
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Last name ...')})
    )
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': _('Email ...')})
    )

    # Set the file field
    avatar = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.jpeg, .jpg, .png',
            'onchange': "document.getElementById('profile-image').src = window.URL.createObjectURL(this.files[0])",
            'class': 'file-input',
        }),
        label='',
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Validate data before saving to database
            self.instance.clean()

        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data
  
    def save(self, commit=True):
        # Update Profile instance
        profile = super().save(commit=False)
        user = profile.user

        # Update user details
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Ensure a simultaneous save to maintain database consistency
        if commit:
            user.save()
            profile.save()

        return profile