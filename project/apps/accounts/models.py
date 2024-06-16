from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from pathlib import Path

# Profile image file name
def image_file_path(instance, filename):
    # Define profile image file name
    profile_image = f'profile_{instance.user.id}.png'
    path = Path(instance.avatar.path).cwd() / 'media/profile_avatars' / profile_image

    # Delete existing image file if it exists
    if path.is_file():
        path.unlink(missing_ok=True)

    return Path('profile_avatars', profile_image)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to=image_file_path)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):

        # Save the profile first
        super().save(*args, **kwargs)
        
        # Resize image and convert to png format
        try:
            size = (300, 300)
            # Open image file
            with Image.open(self.avatar.path) as img:
                # Create a thumbnail
                img.thumbnail(size)
                # Overwrite existing image file according to png format
                img.save(self.avatar.path, "png")
        except OSError:
            print(f"Cannot create thumbnail for {self.avatar.path}")

