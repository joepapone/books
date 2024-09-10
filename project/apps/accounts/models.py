from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
from io import BytesIO
from pathlib import Path
import logging

# Application modules
from apps.books.validators import validate_file_size, validate_image

# Applications models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        _('Avatar'),
        upload_to='avatars/', default='avatar.png', null=True,
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image
        ])

    def save(self, *args, **kwargs):
        # Generate the filename based on user pofile
        filename = f"{self.user.id}_profile.png"
        filepath = Path(settings.MEDIA_ROOT, 'avatars', filename)
        logging.debug(f"Storage file path: {filepath}")
        
        # Check if a new image file has been uploaded
        if not filename.lower() in self.avatar.name.lower():
            # Delete existing file if it exists
            if filepath.is_file():
                filepath.unlink(missing_ok=True)
                logging.debug(f"Deleted old avatar: {filepath}")

            try:
                with Image.open(self.avatar) as img:
                    # Resize to a thumbnail
                    img.thumbnail((200, 300))
                    
                    # Convert the image to PNG
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    
                    # Save the converted image back to the ImageField
                    self.avatar.save(filename, ContentFile(img_io.getvalue()), save=False)
                    logging.debug(f"New avatar saved: {filename}")

            except (OSError, AttributeError, ValueError) as e:
                logging.error(f"Failed to process avatar for user {self.user.username}: {e}")
                # Fallback to a default image
                self._set_default_avatar()

        # Save instance file path to database
        super().save(*args, **kwargs)
    
    def _set_default_avatar(self):
        try:
            with Image.open(Path(settings.MEDIA_ROOT, 'avatar.png')) as img:
                img.thumbnail((200, 300))
                img_io = BytesIO()
                img.save(img_io, format='PNG')
                self.avatar.save(f"{self.user.id}_profile.png", ContentFile(img_io.getvalue()), save=False)
                logging.debug(f"Default avatar used for user {self.user.username}")

        except FileNotFoundError as e:
            logging.error(f"Default avatar not found: {e}")

    def __str__(self):
        return self.user.username
  