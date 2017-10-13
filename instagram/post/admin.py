from django.contrib import admin

from .models import PostComment, Post

admin.site.register(Post)
admin.site.register(PostComment)
