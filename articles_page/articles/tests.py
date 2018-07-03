from django.test import TestCase


class LoginTestCase(TestCase):
    def test_login_redirect(self):
        response = self.client.get('/articles/new_article')
        self.assertRedirects(response, '/articles/login?next=/articles/new_article')
