# Moschitta Auth Documentation

The `moschitta-auth` package provides authentication functionality for the Moschitta Framework, enabling developers to implement user authentication and authorization in their applications.

## Installation

You can install `moschitta-auth` via pip:

```bash
pip install moschitta-auth
```

Or use it with Poetry:

```bash
poetry add moschitta-auth
```

## Usage

### Authenticator Initialization

To use `moschitta-auth`, you need to initialize an instance of the `BasicAuthenticator` class with the path to the database where user information is stored.

```python
from moschitta_auth.basic_authenticator import BasicAuthenticator

# Initialize the authenticator with the path to the database
authenticator = BasicAuthenticator(db_path='auth.db')
```

### User Registration

You can use the `register_user` method of the `BasicAuthenticator` class to register a new user.

```python
# Register a new user
authenticator.register_user(username='john_doe', password='password123')
```

### User Authentication

Authenticate users using the `authenticate_user` method of the `BasicAuthenticator` class.

```python
# Authenticate a user
authenticated = authenticator.authenticate_user(username='john_doe', password='password123')
```

### Access Control

After authentication, you can implement access control logic based on user roles and permissions.

```python
if authenticated:
    # Allow access to restricted resources
    ...
else:
    # Redirect to login page or deny access
    ...
```

## API Reference

### `moschitta_auth.basic_authenticator.BasicAuthenticator`

- `__init__(db_path: str)`: Initializes the authenticator with the path to the database.
- `register_user(username: str, password: str) -> None`: Registers a new user with the provided username and password.
- `authenticate_user(username: str, password: str) -> bool`: Authenticates a user with the provided username and password.
- `__len__() -> int`: Returns the total number of registered users in the database.

## Contributing

Contributions to `moschitta-auth` are welcome! You can contribute by opening issues for bugs or feature requests, submitting pull requests, or helping improve the documentation.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
