from django.db import models


class Post(models.Model):
    photo = models.ImageField(upload_to='photo')
    created_date = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
