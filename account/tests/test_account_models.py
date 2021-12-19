import pytest


class TestCustomerModel:

    def test_customer_str(self, customer):
        """Test the customer string representation"""

        assert customer.__str__() == 'usertest'

    def test_customer_str(self, adminuser):
        """Test the customer string representation"""

        assert adminuser.__str__() == 'admin_user'

    def test_customer_email_no_input(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='')
        assert str(e.value) == 'Customer Account: You must provide an email address'

    def test_customer_email_incorrect(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='a.com')
        assert str(e.value) == 'You must provide an email address'

    def test_adminuser_email_no_input(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='', is_superuser=True, is_staff=True)
        assert str(e.value) == 'Superuser Account: You must provide an email address'

    def test_adminuser_email_incorrect(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='a.com', is_superuser=True, is_staff=True)
        assert str(e.value) == 'You must provide an email address'

    def test_adminuser_email_not_staff(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='', is_superuser=True, is_staff=False)
        assert str(e.value) == 'Superuser must be assigned to is_staff=True.'

    def test_adminuser_email_not_superuser(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='a.com', is_superuser=False, is_staff=True)
        assert str(e.value) == 'Superuser must be assigned to is_superuser=True.'

    def test_adminuser_email_not_active(self, customer_factory):
        with pytest.raises(ValueError) as e:
            customer_factory.create(email='a.com', is_superuser=True, is_staff=True, is_active=False)
        assert str(e.value) == 'Superuser must be assigned to is_active=True.'


class TestAddressModel:

    def test_address_str(self, address):
        """Test the address string representation"""

        name = address.full_name
        assert address.__str__() == f'{name} Address'
