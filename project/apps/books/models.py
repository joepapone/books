from django.db import models
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
from pathlib import Path
from django.urls import reverse
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location="/media/books")


# --- Up load image to authors
def upload_to_authors(instance, filename):
    # Define file name
    filename = f'{instance.id}.png'
    path = Path(instance.headshot.path).cwd() / 'media/authors' / filename
    print(f'test 1: {instance.headshot.path}')

    # Delete existing file if it exists
    if path.is_file():
        path.unlink(missing_ok=True)
    
    return Path('authors', filename)


# --- Up load image to books
def upload_to_books(instance, filename):
    # Define file name
    filename = f'{instance.isbn}.png'
    path = Path(instance.image.path).cwd() / 'media/books' / filename
    print(f'test 1: {instance.image.path}')

    # Delete existing file if it exists
    if path.is_file():
        path.unlink(missing_ok=True)
    
    return Path('books', filename)


# --- Set default copywrite year
def current_year():
    return datetime.today().year


class Section(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, Romance etc.)")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('name'),
                name='genre_unique',
                violation_error_message = "Genre already exists"
            ),
        ]

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.name}'


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    headshot = models.ImageField(upload_to=upload_to_authors, default='author.png', null=True)
    summary = models.TextField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name"]

    def save(self, *args, **kwargs):
        # Save image file
        super().save(*args, **kwargs)
        
        try:
            print(f'test 2: {self.headshot.path}')
            size = (200, 200)
            with Image.open(self.headshot.path) as img:
                # Create an image thumbnail
                img.thumbnail(size)
                # Overwrite existing file and convert to png format
                img.save(self.headshot.path, "png")

        except OSError:
            print(f"Cannot create thumbnail for {self.headshot.path}")
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'    


class Rating(models.Model):
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating}'


class Status (models.Model):

    STATUS_CHOICES = {
        'a': "Available",
        'w': "Wish",
        't': "To read",
        'r': "Reserved",
        'l': "Loaned",
        's': "Sold",
        'n': "Not found",
    }

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, default='a', help_text='Status ...')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-status"]

    def __str__(self):
        return f'{self.get_status_display()}'


def get_sentinel_rating():
    rating = Rating.objects.get_or_create()

    print(f'Sentinel {rating.id}')
    return 1

class Book(models.Model):
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='ISBN ...')
    title = models.CharField(max_length=255, help_text='Title ...')
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, blank=True, null=True)
    copyright = models.PositiveIntegerField(null=True, default=current_year)
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT, blank=True, null=True)
    edition = models.IntegerField(default=1, null=True)

    CATEGORY_CHOICES = {
        'f': "Fiction",
        'n': "Non-fiction",
        'c': "Children's",
    }

    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, blank=True, default='f', help_text='Book category')
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT, blank=True, null=True)
    language = models.CharField(max_length=7, choices=LANGUAGES, blank=True, null=True)
    comments = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=upload_to_books, default='book.png', null=True)
    rating = models.ForeignKey(Rating, on_delete=models.RESTRICT, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('isbn'),
                name='isbn_unique',
                violation_error_message = "ISBN already exists"
            ),
        ]

    def save(self, *args, **kwargs):
        # Save image file
        super().save(*args, **kwargs)
        
        try:
            print(f'test 2: {self.image.path}')
            size = (200, 300)
            with Image.open(self.image.path) as img:
                # Create an image thumbnail
                img.thumbnail(size)
                # Overwrite existing file and convert to png format
                img.save(self.image.path, "png")

        except OSError:
            print(f"Cannot create thumbnail for {self.image.path}")
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.title}'


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class Volume(models.Model):
    collection = models.ManyToManyField("Collection")
    book = models.OneToOneField("Book", on_delete=models.CASCADE)
    number = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f'{self.collection.name} ({self.number})'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.book.title}'
    

'''

import uuid

def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/{filename}"

class UploadedFile(models.Model):
    file = models.FileField(upload_to=generate_filename)
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    
def image_file_path(instance):
    # Define image file name
    image = f'{instance.book.isbn}.png'
    path = Path(instance.image.path).cwd() / 'media/books' / image

    # Delete existing image file if it exists
    if path.is_file():
        path.unlink(missing_ok=True)

    print(f'Test 5 - Path {path} - image {image}')

    return Path('books', image)


def set_filename(instance, filename):
    filename = f'{instance.isbn}.png'
    return f'uploads/{filename}'


CREATE TABLE titles (
    isbn VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author_id INT(5) NOT NULL,
    copyright DATE, 
    publisher_id INT(5) NOT NULL,
    publisher_edition INT(4),
    category_id INT(5) NOT NULL,

    collection_id INT(5) NOT NULL DEFAULT 0,
    volume INT(4),
    section_id INT(5) NOT NULL DEFAULT 0,
    rating INT(5) NOT NULL,
    price DECIMAL(19,2),
    status_id INT(5) NOT NULL,
    comments TEXT,
    image_file VARCHAR(255) NOT NULL, 

    title_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (isbn)
);

CREATE TABLE status(
    status_id INT(5) NOT NULL AUTO_INCREMENT,
    status_name VARCHAR(255) NOT NULL,
    status_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (status_id)
);

-- Auto insert predefined data into tables
INSERT INTO 
    sections(section_name)
VALUES 
    ('Literature'),
    ('Technical'),
    ('Kids');

INSERT INTO 
    status(status_name)
VALUES 
    ('Whish'),
    ('Have'),
    ('To read'),
    ('Loaned');


'''




