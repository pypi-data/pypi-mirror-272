# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moschitta_routing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'moschitta-routing',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Certainly! Below is a template for documentation for the `moschitta-routing` package:\n\n---\n\n# Moschitta Routing Documentation\n\nThe `moschitta-routing` package provides a simple and flexible routing system for the Moschitta Framework, allowing developers to define and handle HTTP routes easily.\n\n## Installation\n\nYou can install `moschitta-routing` via pip:\n\n```bash\npip install moschitta-routing\n```\n\n## Usage\n\n### Creating Routes\n\nRoutes are created using the provided decorators (`@GET`, `@POST`, `@PUT`, `@PATCH`, `@DELETE`, `@OPTIONS`, `@HEAD`, `@CONNECT`, `@TRACE`) and registered with the router.\n\n```python\nfrom moschitta_routing import GET, POST\n\n@GET(\'/users\')\ndef get_users(request):\n    # Handler logic to retrieve users\n    return [{"id": 1, "name": "John"}, {"id": 2, "name": "Alice"}]\n\n@POST(\'/users\')\ndef create_user(request):\n    # Handler logic to create a new user\n    return {"message": "User created successfully"}\n```\n\n### Handling Requests\n\nHandlers are simple functions that take a request object as input and return a JSON response. You can access request parameters within the handler function.\n\n```python\ndef get_users(request):\n    # Handler logic to retrieve users\n    return [{"id": 1, "name": "John"}, {"id": 2, "name": "Alice"}]\n```\n\n### Running the Router\n\nAfter defining routes and handlers, you can run the router to handle incoming HTTP requests.\n\n```python\nfrom moschitta_routing.router import Router\n\nrouter = Router()\n\n# Add routes here using the provided decorators\n\nif __name__ == "__main__":\n    # Run the router\n    router.run(host=\'0.0.0.0\', port=8000)\n```\n\n## API Reference\n\n### `moschitta_routing.router.Router`\n\n- `add_route(path: str, method: str, handler: Callable[[Any], Any]) -> None`: Adds a new route to the router.\n- `get(path: str, method: str = \'GET\') -> Optional[Callable[[Any], Any]]`: Retrieves the handler function associated with a specific route.\n- `__len__() -> int`: Returns the total number of routes currently defined in the router.\n- `__iter__()`: Allows iterating over all registered route paths in the router.\n\n### Decorators\n\n- `@GET(path: str) -> Callable`: Decorator for handling GET requests.\n- `@POST(path: str) -> Callable`: Decorator for handling POST requests.\n- `@PUT(path: str) -> Callable`: Decorator for handling PUT requests.\n- `@PATCH(path: str) -> Callable`: Decorator for handling PATCH requests.\n- `@DELETE(path: str) -> Callable`: Decorator for handling DELETE requests.\n- `@OPTIONS(path: str) -> Callable`: Decorator for handling OPTIONS requests.\n- `@HEAD(path: str) -> Callable`: Decorator for handling HEAD requests.\n- `@CONNECT(path: str) -> Callable`: Decorator for handling CONNECT requests.\n- `@TRACE(path: str) -> Callable`: Decorator for handling TRACE requests.\n\n## Contributing\n\nContributions to `moschitta-routing` are welcome! You can contribute by opening issues for bugs or feature requests, submitting pull requests, or helping improve the documentation.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n\n\n',
    'author': 'Skyler Saville',
    'author_email': 'skylersaville@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
