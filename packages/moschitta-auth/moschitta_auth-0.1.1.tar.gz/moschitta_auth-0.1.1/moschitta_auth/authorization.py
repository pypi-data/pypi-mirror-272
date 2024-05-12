# authorization.py

import pytest

from moschitta_auth.basic_authenticator import BasicAuthenticator


@pytest.fixture
def authenticator():
    return BasicAuthenticator()


def test_authorization_success(authenticator):
    # Simulate successful authorization
    user = {}  # Mock user object
    permissions = ["read"]  # Mock permissions
    assert authenticator.authorize(user, permissions) is True


def test_authorization_failure(authenticator):
    # Simulate failed authorization
    user = {}  # Mock user object
    permissions = ["write"]  # Mock permissions
    assert authenticator.authorize(user, permissions) is False
