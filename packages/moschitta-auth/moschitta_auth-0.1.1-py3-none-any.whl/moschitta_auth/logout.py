# logout.py

import pytest

from moschitta_auth.basic_authenticator import BasicAuthenticator


@pytest.fixture
def authenticator():
    return BasicAuthenticator()


def test_logout(authenticator):
    # Simulate user logout
    request = {}  # Mock request object
    authenticator.logout(request)
    # Assertion for logout action, if any
    assert True  # Placeholder assertion
