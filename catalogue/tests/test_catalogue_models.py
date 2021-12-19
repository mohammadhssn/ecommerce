import pytest

from django.urls import reverse


class TestCategoryModel:

    def test_category_str(self, product_category):
        """Test the category string representation"""

        assert product_category.__str__() == 'django'

    def test_category_reverse(self, client, product_category):
        """Test the category retrieve a list of category"""

        category = product_category
        url = reverse('catalogue:category_list', args=[category.slug])
        response = client.get(url)

        assert response.status_code == 200


class TestProductTypeModel:

    def test_product_type_str(self, product_type):
        """Test the category string representation"""

        assert product_type.__str__() == 'book'


class TestProductSpecification:

    def test_product_specification_str(self, product_specification):
        """Test the category string representation"""

        assert product_specification.__str__() == 'pages'


class TestProduct:

    def test_product_str(self, product):
        """Test the category string representation"""

        assert product.__str__() == 'Product_title'

    def test_product_reverse(self, client, product):
        """Test the retrieve a detail of product"""

        slug = product.slug
        url = reverse('catalogue:product_detail', args=[slug])
        response = client.get(url)

        assert response.status_code == 200


class TestProductSpecificationValue:

    def test_product_specification_value_str(self, product_specification_value):
        """Test the ProductSpecificationValue string representation"""

        assert product_specification_value.__str__() == '250'
