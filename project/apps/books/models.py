from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200, null=True, blank=True)
    headshot = models.ImageField(upload_to="author_headshots")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author")
    copyright = models.CharField(max_length=100)
    publisher = models.ManyToManyField("Publisher")
    edition = models.IntegerField()
    category = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
