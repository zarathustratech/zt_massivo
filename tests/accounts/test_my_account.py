import json

import pytest
from rest_framework.test import APIClient
from tests.helpers import create_test_account

pytestmark = pytest.mark.django_db


def test_my_account():
    client = APIClient()
    password = 'secret12345'
    user = create_test_account(password=password)
    user.first_name = 'Francisco'
    user.last_name = 'Ceruti'
    user.company = 'Guide Post'
    user.save()

    client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
    response = client.get('/api/accounts/me/')

    account_obj = json.loads(response.content)
    assert account_obj['first_name'] == 'Francisco'
    assert account_obj['last_name'] == 'Ceruti'
    assert account_obj['company'] == 'Guide Post'

