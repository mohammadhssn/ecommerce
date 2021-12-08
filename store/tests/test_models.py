from django.test import TestCase
from store.models import Category, Product
from django.contrib.auth import get_user_model


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(
            name='django',
            slug='django'
        )

    def test_category_model_entry(self):
        """Test Category model data insertion/types/field attributes"""

        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')


class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(
            name='django',
            slug='django'
        )
        get_user_model().objects.create(username='admin', password='pass123')
        self.data1 = Product.objects.create(
            category_id=1, title='django beginners', created_by_id=1, slug='django-beginners',
            price='20.00', image='django'
        )

    def test_product_model_entry(self):
        """Test Product model data insertion/types/field attributes"""

        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')
