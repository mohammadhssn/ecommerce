import pytest

from django.urls import reverse


class TestCatalogueViews:

    @pytest.mark.django_db
    def test_root_url(self, client):
        """Test access to homepage"""

        url = reverse('catalogue:store_home')
        response = client.get(url)

        assert response.status_code == 200
