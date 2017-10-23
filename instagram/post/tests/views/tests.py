from django.test import TestCase
from django.urls import reverse, resolve

from ... import views


class PostListToggleViewTest(TestCase):
    TEST_POST_PK = 1
    VIEW_URL = f'/post/{TEST_POST_PK}/like_toggle/'
    VIEW_URL_NAME = 'post:post_like_toggle'

    def test_url_equal_reverse_url_name(self):
        """
        VIEW_URL_NAME을 reverse해서 만든 URL이
        VIEW_URL과 같은지 테스트
        :return:
        """
        self.assertEqual(self.VIEW_URL, reverse(self.VIEW_URL_NAME, kwargs={'post_pk': 1}))

    def test_url_resolves_to_post_like_toggle_view(self):
        """
        VIEW_URL_NAME을 reverse한 (또는 VIEW_URL자체에 해당하는 view가 실제 views.post_like_toggle 뷰를 가르키는지 테스트
        :return:
        """

        found = resolve(self.VIEW_URL)
        self.assertEqual(found.func, views.post_like_toggle)