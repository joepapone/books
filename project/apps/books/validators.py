from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from datetime import datetime
from PIL import Image
import re
import unicodedata


# --- Validation functions
def current_year():
    return datetime.now().year

def isbn13_validator(value):
    """
    Validate the provided ISBN-13.
    The ISBN-13 is a 13-digit number with a specific checksum validation.
    """
    # Check if value matches the pattern of 13 digits
    if not re.match(r'^\d{13}$', value):
        raise ValidationError(
            _('Invalid ISBN-13 format.'),
            code='invalid_format'
        )
    
    # Compute the checksum using the ISBN-13 algorithm
    total = sum((3 if i % 2 else 1) * int(num) for i, num in enumerate(value[:12]))
    check_digit = (10 - (total % 10)) % 10
    
    # Validate the check digit
    if check_digit != int(value[-1]):
        raise ValidationError(
            _('Invalid ISBN-13 checksum.'),
            code='invalid_checksum'
        )
    
def normalize_text(text):
    """
    Normalize the given text by converting to lowercase, removing diacritics,
    special characters, and normalizing spaces.
    """
    if not text:
        return text

    # Convert to lowercase
    normalized_text = text.lower()

    # Decompose Unicode characters (e.g., ä -> a)
    normalized_text = unicodedata.normalize('NFKD', normalized_text)

    # Remove diacritics (accents) by filtering out combining characters
    normalized_text = ''.join(c for c in normalized_text if not unicodedata.combining(c))

    # Remove special characters and normalize spaces
    normalized_text = re.sub(r'[^\w\s]', '', normalized_text)
    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

    return normalized_text

def validate_unique_field(model, field_name, value, user=None, instance=None):
    """
    Validates that the normalized value of the given field is unique within the model.
    Excludes the current instance (if provided) during updates.
    """
    # Normalize the value
    normalized_value = normalize_text(value)

    # Build the queryset
    if instance and instance.pk:
        queryset = model.objects.filter(user=user).exclude(pk=instance.pk)
    else:
        queryset = model.objects.filter(user=user)

    # Fetch and normalize all existing field values for this user
    existing_values = queryset.values_list(field_name, flat=True)
    normalized_existing_values = [
        normalize_text(existing_value) for existing_value in existing_values
    ]

    # Check if the normalized input value already exists
    if normalized_value in normalized_existing_values:
        raise ValidationError(_(f'A {model._meta.verbose_name} with this {field_name} already exists!'))

    return value

def validate_file_size(file):
    """
    Validate uploaded image file size to constraint resources.
    """

    path = Path(file.path)
    if path.is_file():
        max_size_mb = 2 # 2MB
        if file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"Max. upload file size {max_size_mb} MB.")

def validate_image(file):
    """
    Validate uploaded image type to ensure it's an image, with format jpeg, jpg and png.
    """
        
    try:
        # Open the image file
        img = Image.open(file)

        # Verify that the file is indeed an image
        img.verify()
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            raise ValidationError(_('Unsupported image format.'))
        
    except (IOError, SyntaxError) as e:
        raise ValidationError(_('Invalid image file.'))
    
def current_year():
    """
    Get current year.
    """
    return datetime.today().year