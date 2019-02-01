import json

import pytest

from tests.helpers import create_test_account

pytestmark = pytest.mark.django_db


def test_login(client):
    password = 'secret12345'
    user = create_test_account(password=password)
    post_kwargs = {'email': user.email, 'password': password}
    response = client.post(
        '/api/accounts/auth/login/',
        post_kwargs)

    assert json.loads(response.content)['key'] == user.auth_token.key
