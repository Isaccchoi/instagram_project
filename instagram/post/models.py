from django.conf import settings
from django.db import models


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author__isnull=True)


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    # 새로만든 PostManager를 기본 모델 매니저인 objects를 대신해서 사용
    objects = PostManager()

    class Meta:
        ordering = ['-created_date', ]

    def __str__(self):
        return f'Post (PK: {self.pk})'


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_date', ]

    def __str__(self):
        return f"{self.post.pk} - {self.content}"
