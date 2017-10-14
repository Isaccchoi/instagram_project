from django.db import models


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk


class PostComment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.pk} - {self.content}"
