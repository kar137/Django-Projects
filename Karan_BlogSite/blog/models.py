from django.db import models

# Create your models here.

class Post(models.Model):
    Title = models.CharField(max_length=50)
    Excerpt = models.CharField(max_length=50)
    ImageName = models.CharField(max_length=100)
    Date = models.DateField()
    slug = models.SlugField()
    content = models.CharField(max_length=1000)

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()

class Tag(models.Model):
    caption = models.CharField(max_length=50)