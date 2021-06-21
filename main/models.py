from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=20)
    contents = models.TextField(blank=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="posts")
