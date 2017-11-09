import io
from random import randint

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from post.apis import PostListView
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostListView

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username, age=0)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(
            resolver_match.url_name,
            self.URL_API_POST_LIST_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS)

    def test_post_list(self):
        # Post object생성을 위하여 dummy user 생성
        author = self.create_user()
        num = randint(1, 20)
        for i in range(num):
            self.create_post(author=author)
        url = reverse(self.URL_API_POST_LIST_NAME)
        # url에 get요청을 하여 response를 받음
        response = self.client.get(url)
        # 정상적으로 url에 접근하여 status_code가 200이 뜨는지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Post.objects.count가 랜덤으로 생성으로 한 갯수인 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response된 데이터의 갯수가 num과 같은지 확인
        self.assertEqual(len(response.data), num)
        # 만들어진 post 안에 pk, author, photo, created_date 키값이 있는지 확인
        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_date', cur_post_data)

    def test_get_post_list_exclude_if_author_is_none(self):
        """
        author가 none인경우 안나오는지 테스트
        """
        author = self.create_user()
        num_author_none_posts = randint(0, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=author)

        response = self.client.get(self.URL_API_POST_LIST)
        self.assertEqual(len(response.data), num_posts)

    def test_create_post(self):
        """
        Post Create가 되는지 확인
        """
        # PostListView를 reverse를 이용해 url을 받아옴
        url = reverse(self.URL_API_POST_LIST_NAME)
        # user 생성
        user = self.create_user()
        # force_login을 이용해 생성한 user로그인
        self.client.force_login(user=user)

        # dummy file 생서
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        data = {
            'photo': file,
        }
        # post방식으로 url에 dummy file 전달
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertIn('photo', response.data)
        self.assertIn('pk', response.data)
        self.assertEqual(1, response.data['pk'])