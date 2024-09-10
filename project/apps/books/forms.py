from django import forms
from django.db.models import OuterRef, Subquery, CharField, Value
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Application modules
from apps.books.models import Book, Author, Publisher, Genre, Price, Rating, Status, Collection, Section

# Application forms
class BookForm(forms.ModelForm):
    # Set the field for mixin validation
    title_field = 'title'
    
    # Set the file field
    cover_image = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.jpeg, .jpg, .png',
            'onchange': "document.getElementById('cover_image').src = window.URL.createObjectURL(this.files[0])",
            'class': 'file-input',
        }),
        label='',
        required=False
    )

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'copyright', 'publisher', 'edition', 'category', 'genre', 'language', 'collection', 'volume_number', 'comments', 'cover_image' ]
    
    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['isbn'].widget.attrs.update({'placeholder': _('ISBN 13 code ...')})
        self.fields['title'].widget.attrs.update({'placeholder': _('Title ...')})
        self.fields['copyright'].widget.attrs.update({'placeholder': _('Copyright ...')})
        self.fields['edition'].widget.attrs.update({'placeholder': _('Edition ...')})
        self.fields['comments'].widget.attrs.update({'placeholder': _('Comments ...')})

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data

class AuthorForm(forms.ModelForm):
    # Set the field for mixin validation
    name_field = 'name'
    
    # Set the file field
    headshot = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.jpeg, .jpg, .png',
            'onchange': "document.getElementById('headshot-image').src = window.URL.createObjectURL(this.files[0])",
            'class': 'file-input',
        }),
        label='',
        required=False
    )

    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'date_of_death', 'summary', 'headshot']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['name'].widget.attrs.update({'placeholder': _('Name ...')})
        self.fields['summary'].widget.attrs.update({'placeholder': _('Summary ...')})
   
    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data

class PublisherForm(forms.ModelForm):
    # Set the field for mixin validation
    name_field = 'name'

    class Meta:
        model = Publisher
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['name'].widget.attrs.update({'placeholder': _('Name ...')})
        self.fields['description'].widget.attrs.update({'placeholder': _('Description ...')})

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data
    
class GenreForm(forms.ModelForm):
    # Set the field for mixin validation
    name_field = 'name'

    class Meta:
        model = Genre
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['name'].widget.attrs.update({'placeholder': _('Name ...')})
        self.fields['description'].widget.attrs.update({'placeholder': _('Description ...')})

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data
    
class CollectionForm(forms.ModelForm):
    # Set the field for mixin validation
    name_field = 'name'

    class Meta:
        model = Collection
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['name'].widget.attrs.update({'placeholder': _('Name ...')})
        self.fields['description'].widget.attrs.update({'placeholder': _('Description ...')})

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data

class SectionForm(forms.ModelForm):
    # Set the field for mixin validation
    name_field = 'name'

    class Meta:
        model = Section
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        # Initialize the form
        super().__init__(*args, **kwargs)

        # Add placeholders or any other widget tweaks
        self.fields['name'].widget.attrs.update({'placeholder': _('Name ...')})
        self.fields['description'].widget.attrs.update({'placeholder': _('Description ...')})

    def clean(self):
        cleaned_data = super().clean()

        # Assign the user to the instance
        self.instance.user = self.user

        print(f"User - form {self.instance.user}")

        try:
            # Call model's clean method to validate
            self.instance.clean()
        except ValidationError as e:
            for field, error in e.message_dict.items():
                self.add_error(field, error)

        return cleaned_data

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['currency', 'purchase_price', 'price_source', 'purchase_date', 'sale_price']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.HiddenInput(),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (0 <= rating <= 5):
            raise forms.ValidationError(_('Rating must be between 0 and 5.'))
        return rating

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']

    def clean_status(self):
        status = self.cleaned_data.get('status')

        # Validate choices
        valid_statuses = [choice[0] for choice in Status.STATUS_CHOICES]

        if status not in valid_statuses:
            raise forms.ValidationError(_('Invalid status selected.'))

        return status

class BookSelectionForm(forms.Form):
    books = forms.ModelMultipleChoiceField(
        queryset=Book.objects.none(),  # Start with an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If a user is provided, filter the books by the current user
        if user is not None:                   
            # Subquery to get the status for each book for the current user
            status_subquery = Status.objects.filter(
                book=OuterRef('pk'),
                user=user
            ).values('status')[:1]

            # Annotate each book with the user rating and book status
            queryset = Book.objects.annotate(
                status=Coalesce(Subquery(status_subquery, output_field=CharField()), Value(''))
            )

            # Apply filters, books with status in the specified list
            self.fields['books'].queryset = queryset.filter(status__in=[ 't', 'a', 'r', 'l'])
