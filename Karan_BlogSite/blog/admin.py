from django.contrib import admin
from .models import Post, Author, Tag

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "Date", "tag",)
    list_display = ("Title", "Date", "author",)
    prepopulated_fields = {"slug": ("Title", )}

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
