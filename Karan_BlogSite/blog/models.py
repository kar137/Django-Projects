from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption

class Post(models.Model):
    Title = models.CharField(max_length=150)
    Excerpt = models.CharField(max_length=200)
    ImageName = models.CharField(max_length=100)
    Date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")

    tag = models.ManyToManyField(Tag)
