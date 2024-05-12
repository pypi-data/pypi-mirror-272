# helper_functions.py


def authenticate_request(authenticator, request):
    """Authenticate the incoming request using the specified authenticator."""
    return authenticator.authenticate(request)


def authorize_user(authenticator, user, permissions):
    """Authorize the user based on the specified permissions."""
    return authenticator.authorize(user, permissions)


def logout_user(authenticator, request):
    """Logout the user using the specified authenticator."""
    return authenticator.logout(request)
