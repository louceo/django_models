from django.contrib import admin
from .models import Post, Category, PostCategory, Author, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)