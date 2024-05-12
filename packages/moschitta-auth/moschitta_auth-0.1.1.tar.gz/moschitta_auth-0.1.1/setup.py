# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moschitta_auth']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=4.1.3,<5.0.0']

setup_kwargs = {
    'name': 'moschitta-auth',
    'version': '0.1.1',
    'description': '',
    'long_description': "# Moschitta Auth Documentation\n\nThe `moschitta-auth` package provides authentication functionality for the Moschitta Framework, enabling developers to implement user authentication and authorization in their applications.\n\n## Installation\n\nYou can install `moschitta-auth` via pip:\n\n```bash\npip install moschitta-auth\n```\n\nOr use it with Poetry:\n\n```bash\npoetry add moschitta-auth\n```\n\n## Usage\n\n### Authenticator Initialization\n\nTo use `moschitta-auth`, you need to initialize an instance of the `BasicAuthenticator` class with the path to the database where user information is stored.\n\n```python\nfrom moschitta_auth.basic_authenticator import BasicAuthenticator\n\n# Initialize the authenticator with the path to the database\nauthenticator = BasicAuthenticator(db_path='auth.db')\n```\n\n### User Registration\n\nYou can use the `register_user` method of the `BasicAuthenticator` class to register a new user.\n\n```python\n# Register a new user\nauthenticator.register_user(username='john_doe', password='password123')\n```\n\n### User Authentication\n\nAuthenticate users using the `authenticate_user` method of the `BasicAuthenticator` class.\n\n```python\n# Authenticate a user\nauthenticated = authenticator.authenticate_user(username='john_doe', password='password123')\n```\n\n### Access Control\n\nAfter authentication, you can implement access control logic based on user roles and permissions.\n\n```python\nif authenticated:\n    # Allow access to restricted resources\n    ...\nelse:\n    # Redirect to login page or deny access\n    ...\n```\n\n## API Reference\n\n### `moschitta_auth.basic_authenticator.BasicAuthenticator`\n\n- `__init__(db_path: str)`: Initializes the authenticator with the path to the database.\n- `register_user(username: str, password: str) -> None`: Registers a new user with the provided username and password.\n- `authenticate_user(username: str, password: str) -> bool`: Authenticates a user with the provided username and password.\n- `__len__() -> int`: Returns the total number of registered users in the database.\n\n## Contributing\n\nContributions to `moschitta-auth` are welcome! You can contribute by opening issues for bugs or feature requests, submitting pull requests, or helping improve the documentation.\n\n## License\n\nThis project is licensed under the terms of the [MIT License](LICENSE).\n",
    'author': 'Skyler Saville',
    'author_email': 'skylersaville@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
