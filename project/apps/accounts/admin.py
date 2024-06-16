from django.contrib import admin
from apps.accounts.models import Profile

# Register model to Django Admin app
admin.site.register(Profile)