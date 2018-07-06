from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import UserProfile, Category, Article


class LoginTestCase(TestCase):
    def setUp(self):
        self.valid_user = {
            'username': 'testuser1',
            'password': '1234qwer'}
        self.invalid_user = {
            'username': 'testuser2',
            'password': '1234'}

        User.objects.create_user(**self.valid_user)

    def test_login_positive(self):
        response = self.client.post('/articles/login', self.valid_user, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_login_negative(self):
        response = self.client.post('/articles/login', self.invalid_user, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_logout(self):
        response = self.client.get('/articles/logout', follow=True)
        self.assertFalse(response.context['user'].is_active)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.valid_user = {
            'username': 'testuser1',
            'password1': '1234qwer',
            'password2': '1234qwer',
            'email': 'some@some.com',
            }
        self.invalid_user = {
            'username': 'testuser2',
            'email': 'somemail.com',
            'password1': 'qwer1234',
            'password2': 'qwer1234'
        }

    def test_register_positive(self):
        response = self.client.post('/articles/sign_up', self.valid_user, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_register_negative(self):
        response = self.client.post('/articles/sign_up', self.invalid_user, follow=True)
        self.assertFalse(response.context['user'].is_active)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.valid_number = {
            'telephone': '+380671234567',
             }

        self.invalid_number = {
            'telephone': '+38067123456789',
            }

        self.user = {
            'username': 'testuser1',
            'email': 'some@some.com',
            'password': '1234qwer'}

        User.objects.create_user(**self.user)
        self.user_pk = User.objects.get(username=self.user['username']).pk

    def test_register_positive(self):
        user = UserProfile.objects.get(id=self.user_pk)
        user.telephone = self.valid_number
        user.save()
        self.assertRegexpMatches(user.telephone['telephone'], '^\+380\d{9}$')

    def test_register_negative(self):
        user = UserProfile.objects.get(id=self.user_pk)
        user.telephone = self.invalid_number
        user.save()
        self.assertNotRegexpMatches(user.telephone['telephone'], '^\+380\d{9}$')


class ArticleTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser1',
            'password': '1234qwer',
            'email': 'some@some.com'
        }
        self.staff_user_data = {
            'username': 'staffuser',
            'password': '1234qwer',
            'email': 'some@some.com',
            'is_staff': True,
        }
        self.valid_article = {
            'title': 'title',
            'text': 'text',
            'category': 1,
            'status': 'REVIEW',
        }
        self.invalid_article = {
            'title': 'titletitletitletitle',
            'text': 'text',
            'category': 2,
            'status': 'REVIEW',
        }
        Category.objects.create(name_category='test_category')
        User.objects.create_user(**self.user_data)
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password'])

    def test_create_article_positive(self):
        response = self.client.post('/articles/new_article', self.valid_article, follow=True)
        article_num = Article.objects.all().count()
        self.assertGreater(article_num, 0)

    def test_create_article_negative(self):
        response = self.client.post('/articles/new_article', self.invalid_article, follow=True)
        article_num = Article.objects.all().count()
        self.assertEqual(article_num, 0)

    def test_edit_article(self):
        self.client.post('/articles/new_article', self.valid_article, follow=True)
        user = User.objects.create_user(**self.staff_user_data)
        user.groups.clear()
        group = Group.objects.get(name='Staff group')
        group.user_set.add(user)
        self.client.login(
            username=self.staff_user_data['username'],
            password=self.staff_user_data['password'])
        edit_article = self.valid_article
        edit_article['status'] = 'LIVE'
        response = self.client.post('/articles/1/update', edit_article, follow=True)
        article_num = Article.objects.filter(status='LIVE').count()
        self.assertGreater(article_num, 0)


class AccessTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser1',
            'password': '1234qwer',
            'email': 'some@some.com'
        }
        self.staff_user_data = {
            'username': 'staffuser',
            'password': '1234qwer',
            'email': 'some@some.com',
            'is_staff': True,
        }

        User.objects.create_user(**self.user_data)
        user = User.objects.create_user(**self.staff_user_data)
        user.groups.clear()
        group = Group.objects.get(name='Staff group')
        group.user_set.add(user)

    def test_access_create_article(self):
        self.client.login(username=self.staff_user_data['username'],
                          password=self.staff_user_data['password'])
        response = self.client.get('/articles/new_article')
        self.assertRedirects(response, '/articles/login?next=/articles/new_article')

    def test_access_review_articles(self):
        self.client.login(username=self.user_data['username'],
                          password=self.user_data['password'])
        response = self.client.get('/articles/review_articles')
        self.assertRedirects(response, '/articles/')

    def test_access_add_category(self):
        self.client.login(username=self.user_data['username'],
                          password=self.user_data['password'])
        response = self.client.get('/articles/category/add')
        self.assertRedirects(response, '/articles/login?next=/articles/category/add')

    def test_access_admin_panel(self):
        self.client.login(username=self.user_data['username'],
                          password=self.user_data['password'])
        response = self.client.get('/articles/admin_panel')
        self.assertRedirects(response, '/articles/')
