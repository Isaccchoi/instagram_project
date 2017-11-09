from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory, APILiveServerTestCase
from post.apis import PostListView


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_POST_LIST_NAME)

