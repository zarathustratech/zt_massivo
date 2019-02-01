import pytest
import requests

from apps.accounts.models import Account

pytestmark = pytest.mark.django_db


def test_register_account(client):
    assert Account.objects.count() == 0
    account_data = {
        'first_name': 'Francisco',
        'last_name': 'Ceruti',
        'email': 'test@test.com',
        'password1': 'ABC12341234',
        'password2': 'ABC12341234',
        'company': 'ACME'
    }
    client.post('/api/accounts/auth/register/', account_data)

    assert Account.objects.count() == 1
    account = Account.objects.get()
    assert account.first_name == 'Francisco'
    assert account.last_name == 'Ceruti'
    assert account.email == 'test@test.com'
    assert account.company == 'ACME'
    assert account.password != '1234'
    assert account.is_staff is False
    assert account.is_superuser is False
