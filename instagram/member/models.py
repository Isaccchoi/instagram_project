from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_DJANGO = 'D'
    signup_choices = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(max_length=1, choices=signup_choices)
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    age = models.IntegerField('나이')
    like_posts = models.ManyToManyField('post.Post', verbose_name='좋아요 누른 포스트')
    # 내가 팔로우 하고 있는 목록
    following_users = models.ManyToManyField(
        'self',
        through='Relation',
        through_fields=('from_user', 'to_user'),
        symmetrical=False,
        related_name='followers',
    )
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_users_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return True
        # if user in self.following_users.all():
        #     Relation.objects.filter(from_user=self, to_user=user).delete()
        # else:
        #     self.following_users_relations.create(to_user=user)
        #     Relation.objects.create(from_user=self, to_user=user)


class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='following_users_relations', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_relations', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Relation (from: {self.from_user.username}, (to: {self.to_user.username})'
