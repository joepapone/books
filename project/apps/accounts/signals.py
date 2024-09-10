from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Application models
from apps.accounts.models import Profile

# Applications sigmals
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()