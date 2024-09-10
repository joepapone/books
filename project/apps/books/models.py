from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from datetime import datetime, date
from PIL import Image
from io import BytesIO
from pathlib import Path
import logging

# Application modules
from apps.books.validators import isbn13_validator, validate_unique_field, validate_file_size, validate_image

# *** Still to evaluate ***
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location="/media/books")


# Application models
class Author(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    date_of_birth = models.DateField(_('Born'), null=True, blank=True)
    date_of_death = models.DateField(_('Died'), null=True, blank=True)
    headshot = models.ImageField(
        _('Headshot'),
        upload_to='authors/', default='author.png', null=True,
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image
        ])
    summary = models.TextField(_('Summary'), max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_author_per_user'),
        ]

    def clean(self):
        super().clean()

        # Ensure that the date_of_birth is not in the future
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValidationError({
                'date_of_birth': _('Date of birth cannot be in the future.')
            })
        
        # Ensure that date_of_death is after date_of_birth, if provided
        if self.date_of_birth and self.date_of_death and self.date_of_death < self.date_of_birth:
            raise ValidationError({
                'date_of_death': _('Date of death cannot be before the date of birth.')
            })

        try:
            # Validate uniqueness for name
            validate_unique_field(Author, 'name', self.name, user=self.user, instance=self)

        except ValidationError as e:
            # Attach the error to the respective field
            if 'name' in str(e):
                raise ValidationError({'name': e.message})

    def save(self, *args, **kwargs):
        # Generate the filename based on user and author name
        filename = f"{self.user.id}_author_{self.id}.png"
        filepath = Path(settings.MEDIA_ROOT, 'authors', filename)
        logging.debug(f"Storage file path: {filepath}")

        # Make sure the directory exists
        if not filepath.parent.exists():
            logging.error(f"Directory does not exist: {filepath.parent}")
        
        # Check if file exists before saving
        if filepath.is_file():
            logging.debug(f"File exists: {filepath}")
        else:
            logging.debug(f"File does not exist: {filepath}")
        
        # Check if a new image file has been uploaded
        if not filename.lower() in self.headshot.name.lower():
            # Delete existing file if it exists
            if filepath.is_file():
                filepath.unlink(missing_ok=True)

            try:
                logging.debug(f"Uploaded file: {self.headshot} - type {type(self.headshot)}")
                # Open the uploaded image file
                with Image.open(self.headshot) as img:
                    # Set thumbnail size
                    size = (200, 300)
                    img.thumbnail(size)
                    
                    # Convert the image to PNG
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    
                    # Save the converted image back to the ImageField
                    self.headshot.save(filename, ContentFile(img_io.getvalue()), save=False)

            except (OSError, AttributeError, ValueError) as e:
                logging.error(f"Cannot create thumbnail for {self.headshot.path}: {e}")
                
                # Fallback to a default image
                with Image.open(Path(settings.MEDIA_ROOT, 'author.png')) as img:
                    img.thumbnail(size)
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    self.headshot.save(filename, ContentFile(img_io.getvalue()), save=False)
        
        # Save instance file path to database
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'),max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_publisher_per_user')
        ]

    def clean(self):
        super().clean()

        try:
            # Validate uniqueness for name
            validate_unique_field(Publisher, 'name', self.name, user=self.user, instance=self)
        
        except ValidationError as e:
            # Attach the error to the respective field
            if 'name' in str(e):
                raise ValidationError({'name': e.message})

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True, help_text="Enter a book genre (e.g. Science Fiction, Romance etc.)")
    description = models.TextField(_('Description'), max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_genre_per_user')
        ]

    def clean(self):
        super().clean()

        try:
            # Validate uniqueness for name
            validate_unique_field(Genre, 'name', self.name, user=self.user, instance=self)

        except ValidationError as e:
            # Attach the error to the respective field
            if 'name' in str(e):
                raise ValidationError({'name': e.message})

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.name}'

class Collection(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_collection_per_user')
        ]
 
    def clean(self):
        super().clean()

        try:
            # Validate uniqueness for name
            validate_unique_field(Collection, 'name', self.name, user=self.user, instance=self)

        except ValidationError as e:
            # Attach the error to the respective field
            if 'name' in str(e):
                raise ValidationError({'name': e.message})
    
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_section_per_user')
        ]

    def clean(self):
        super().clean()

        try:
            # Validate uniqueness for name
            validate_unique_field(Section, 'name', self.name, user=self.user, instance=self)

        except ValidationError as e:
            # Attach the error to the respective field
            if 'name' in str(e):
                raise ValidationError({'name': e.message})
    
    def __str__(self):
        return self.name

class Book(models.Model):
    # Define choices as class constants
    FICTION = 'f'
    NON_FICTION = 'n'
    
    CATEGORY_CHOICES = [
        (FICTION, _('Fiction')),
        (NON_FICTION, _('Non-fiction')),
    ]

    isbn = models.CharField(
        _('ISBN'), max_length=13, unique=True, 
        validators=[
            isbn13_validator
        ])
    title = models.CharField(_('Title'), max_length=255)
    author = models.ForeignKey(Author, verbose_name=_('Author'), on_delete=models.RESTRICT, blank=True, null=True)
    copyright = models.PositiveIntegerField(_('Copyright'), null=True, blank=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_('Publisher'), on_delete=models.RESTRICT, blank=True, null=True)
    edition = models.IntegerField(_('Edition'), blank=True, null=True)
    category = models.CharField(_('Category'), max_length=1, choices=CATEGORY_CHOICES, blank=True, default=FICTION)
    genre = models.ForeignKey(Genre, verbose_name=_('Genre'),  on_delete=models.RESTRICT, blank=True, null=True)
    language = models.CharField(_('Language'), max_length=7, choices=LANGUAGES, blank=True, null=True)
    comments = models.TextField(_('Comments'), max_length=500, blank=True, null=True)
    cover_image = models.ImageField(
        _('Cover image'),
        upload_to='books/', default='book.png', null=True,
        validators=[
            validate_file_size,
            validate_image,
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ])
    collection = models.ForeignKey(Collection, verbose_name=_('Collection'), on_delete=models.RESTRICT, blank=True, null=True)
    volume_number = models.PositiveIntegerField(_('Volume Number'), null=True, blank=True)
    section = models.ForeignKey(Section, verbose_name=_('Section'), on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_title_per_user'),
            models.UniqueConstraint(fields=['user', 'isbn'], name='unique_isbn_per_user'),
            models.UniqueConstraint(fields=['collection', 'volume_number'], name='unique_volume_number_per_collection')
        ]
    
    # Converts the annotated status into its display value
    def get_dynamic_status_display(self):
        status_mapping = dict(Status.STATUS_CHOICES)
        return status_mapping.get(self.status, "Unknown Status")

    def clean(self):
        super().clean()

        #Validate copyright year
        if self.copyright:
            current_year = datetime.now().year
            if self.copyright > current_year:
                raise ValidationError({'copyright': _('The copyright year cannot be in the future.')})
            if self.copyright < 1440:
                # Considering the printing press was invented in 1440.
                raise ValidationError({'copyright': _('The copyright year must be after 1440.')})

        try:
            # Validate unique ISBN per user
            validate_unique_field(Book, 'isbn', self.isbn, user=self.user, instance=self)
            # Validate unique title per user
            validate_unique_field(Book, 'title', self.title, user=self.user, instance=self)

        except ValidationError as e:
            # Attach the error to the respective field
            if 'isbn' in str(e):
                raise ValidationError({'isbn': e.message})
            elif 'title' in str(e):
                raise ValidationError({'title': e.message})
            
        # Validate unique volume number within a collection
        if self.collection and self.volume_number:
            if Book.objects.exclude(pk=self.pk).filter(collection=self.collection, volume_number=self.volume_number).exists():
                raise ValidationError({'volume_number': _('Collection with this volume number already exists.')})
            
    def save(self, *args, **kwargs):
        # Convert the title to uppercase before saving
        self.title = self.title.upper()

        # Generate the filename based on user and author name
        filename = f"{self.user.id}_{self.isbn.replace(' ', '_').lower()}.png"
        filepath = Path(settings.MEDIA_ROOT, 'books', filename)
        logging.debug(f"Storage file path: {filepath}")
        
        # Check if a new image file has been uploaded
        if not filename.lower() in self.cover_image.name.lower():
            # Delete existing file if it exists
            if filepath.is_file():
                filepath.unlink(missing_ok=True)

            try:
                logging.debug(f"Uploaded file: {self.cover_image} - type {type(self.cover_image)}")
                # Open the uploaded image file
                with Image.open(self.cover_image) as img:
                    # Set thumbnail size
                    size = (200, 300)
                    img.thumbnail(size)
                    
                    # Convert the image to PNG
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    
                    # Save the converted image back to the ImageField
                    self.cover_image.save(filename, ContentFile(img_io.getvalue()), save=False)

            except (OSError, AttributeError, ValueError) as e:
                logging.error(f"Cannot create thumbnail for {self.cover_image.path}: {e}")
                
                # Fallback to a default image
                with Image.open(Path(settings.MEDIA_ROOT, 'book.png')) as img:
                    img.thumbnail(size)
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    self.cover_image.save(filename, ContentFile(img_io.getvalue()), save=False)
        
        # Save instance file path to database
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Price(models.Model):
        # Define choices with key, name, and symbol
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar', '$'),
        ('EUR', 'Euro', '€'),
        ('GBP', 'British Pound', '£'),
        ('JPY', 'Japanese Yen', '¥'),
        ('AUD', 'Australian Dollar', 'A$'),
        ('CAD', 'Canadian Dollar', 'C$'),
        ('CHF', 'Swiss Franc', 'CHF'),
        ('CNY', 'Chinese Yuan', '¥'),
        ('SEK', 'Swedish Krona', 'kr'),
        ('NZD', 'New Zealand Dollar', 'NZ$'),
        # Add more currencies
    ]

    # Define choices as class constants
    PURCHASE = 'p'
    REFERENCE = 'r'
        
    SOURCE_CHOICES = [
        (PURCHASE, _('Purchase')),
        (REFERENCE, _('Reference')),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='prices')
    currency = models.CharField(_('Currency'), max_length=3, choices=[(key, name) for key, name, symbol in CURRENCY_CHOICES], default='EUR')
    purchase_price = models.DecimalField(_('Purchase price'), max_digits=10, decimal_places=2, null=True, blank=True)
    price_source = models.CharField(_('Price source'), max_length=1, choices=SOURCE_CHOICES, default=PURCHASE)
    purchase_date = models.DateField(_('Purchase date'), null=True, blank=True)
    sale_price = models.DecimalField(_('Sale price'), max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'book']),
        ]
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_price_per_user')
        ]
    
    def get_currency_name(self):
        currency_dict = dict((key, name) for key, name, symbol in self.CURRENCY_CHOICES)
        return currency_dict.get(self.currency, '')

    def get_currency_symbol(self):
        currency_dict = dict((key, symbol) for key, name, symbol in self.CURRENCY_CHOICES)
        return currency_dict.get(self.currency, '')
    
    def __str__(self):
        return f"{self.book.title}{_('- Sale Price: ')}{self.sale_price}"

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'book']),
        ]
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_rating_per_user')
        ]

    def __str__(self):
        return self.rating

class Status(models.Model):
    # Define choices as class constants
    WHISH = 'w'
    TO_READ = 't'
    AVAILABLE = 'a'
    RESERVED = 'r'
    LOANED = 'l'
    FOR_SALE = 'f'
    SOLD = 's'
    NOT_FOUND = 'n'
        
    STATUS_CHOICES = [
        (WHISH, _('Wish')),
        (TO_READ, _('To read')),
        (AVAILABLE, _('Available')),
        (RESERVED, _('Reserved')),
        (LOANED, _('Loaned')),
        (FOR_SALE, _('For sale')),
        (SOLD, _('Sold')),
        (NOT_FOUND, _('Not found')),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_CHOICES, default=AVAILABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'book']),
        ]
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_status_per_user')
        ]
    
    def __str__(self):
        return self.status
