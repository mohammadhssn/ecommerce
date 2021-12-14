from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpRequest
from django.conf import settings

from importlib import import_module
from unittest import skip

from store.views import ProductsAll
from store.models import Category, Product


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='django',
            slug='django'
        )
        get_user_model().objects.create(email='admin@email.com', user_name='admin', password='pass123')
        self.product = Product.objects.create(
            category_id=1, title='django beginners', created_by_id=1, slug='django-beginners',
            price='20.00', image='django'
        )

    def test_url_allowed_hosts(self):
        """Test allowed hosts"""

        response = self.client.get(reverse('store:product_all'), HTTP_HOST='wrong.com')
        self.assertEqual(response.status_code, 400)

        response = self.client.get(reverse('store:product_all'), HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.slug]))

        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.client.get(reverse('store:category_list', args=[self.category.slug]))

        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = ProductsAll.get(self, request)
        html = response.content.decode('utf8')
        self.assertIn('<Title>\n    Bookstore\n</Title>', html.title())
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = ProductsAll.get(self, request)
        html = response.content.decode('utf8')

        self.assertIn('<Title>\n    Bookstore\n</Title>', html.title())
        self.assertEqual(response.status_code, 200)
