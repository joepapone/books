from django.db.models.signals import post_save
from django.dispatch import receiver

# Application modules
from apps.books.models import Book, Rating, Status, Price


# Applications sigmals
@receiver(post_save, sender=Book)
def create_default_rating(sender, instance, created, **kwargs):
    if created:
        Rating.objects.create(book=instance, user=instance.user, rating=0)

@receiver(post_save, sender=Book)
def create_default_status(sender, instance, created, **kwargs):
    if created:
        Status.objects.create(user=instance.user, book=instance, status='a')

@receiver(post_save, sender=Book)
def create_default_price(sender, instance, created, **kwargs):
    if created:
        # Create with default values
        Price.objects.create(
            book=instance,
            currency='EUR',
            purchase_price=0.00,
            sale_price=0.00,
            price_source=Price.PURCHASE,
            user=instance.user
        )