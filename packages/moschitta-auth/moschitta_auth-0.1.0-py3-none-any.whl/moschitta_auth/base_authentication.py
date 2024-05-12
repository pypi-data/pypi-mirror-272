from abc import ABC, abstractmethod


class BaseAuthenticator(ABC):
    """Base class for authentication in the Moschitta framework."""

    @abstractmethod
    def authenticate(self, request):
        """Authenticate the user based on the incoming request.

        Args:
            request: The incoming request object.

        Returns:
            Tuple: A tuple containing (user, credentials) if authentication succeeds, None otherwise.
        """
        pass

    @abstractmethod
    def authorize(self, user, permissions):
        """Authorize the user based on their permissions.

        Args:
            user: The authenticated user object.
            permissions: A list of permissions required for the resource.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        pass

    @abstractmethod
    def logout(self, request):
        """Logout the user and invalidate their session/token.

        Args:
            request: The incoming request object.
        """
        pass
