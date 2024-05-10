from typing import Any, Callable, Optional


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path: str, method: str, handler: Callable[[Any], Any]) -> None:
        """Adds a new route to the router."""
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler

    def get(self, path: str, method: str = "GET") -> Optional[Callable[[Any], Any]]:
        """Retrieves the handler function associated with a specific route."""
        if path in self.routes and method in self.routes[path]:
            return self.routes[path][method]
        return None

    def __getitem__(self, path: str) -> Optional[Callable[[Any], Any]]:
        """Allows accessing handlers using dictionary-like syntax."""
        return self.get(path)

    def __len__(self) -> int:
        """Returns the total number of routes currently defined in the router."""
        return sum(len(methods) for methods in self.routes.values())

    def __iter__(self):
        """Allows iterating over all registered route paths in the router."""
        return iter(self.routes.keys())
