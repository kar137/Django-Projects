from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()

class Tag(models.Model):
    caption = models.CharField(max_length=50)

class Post(models.Model):
    Title = models.CharField(max_length=150)
    Excerpt = models.CharField(max_length=200)
    ImageName = models.CharField(max_length=100)
    Date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(MinLengthValidator(10))

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name="posts")

    tag = models.ManyToManyField(Tag)
