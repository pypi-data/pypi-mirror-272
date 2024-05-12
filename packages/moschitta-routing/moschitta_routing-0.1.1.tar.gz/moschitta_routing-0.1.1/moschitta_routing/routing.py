import json
from http import HTTPStatus
from typing import Any, Callable

from .router import Router

router = Router()

def route(path: str, method: str, handler: Callable[[Any], Any]) -> None:
    """Decorator to add a route to the router."""
    def decorator(func):
        router.add_route(path, method, func)
        return func
    return decorator

def _make_response(data: Any, status_code: int = HTTPStatus.OK) -> str:
    """Helper function to create JSON response."""
    return json.dumps({"data": data}), status_code, {"Content-Type": "application/json"}

def _require_params(required_params: list):
    """Decorator to enforce required parameters for request handlers."""
    def decorator(func):
        def wrapper(request):
            for param in required_params:
                if param not in request:
                    return _make_response({"error": f"Missing required parameter: {param}"}, HTTPStatus.BAD_REQUEST)
            return func(request)
        return wrapper
    return decorator

def _get_required_params(func) -> list:
    """Helper function to extract required parameters from function annotations."""
    return [param for param, annotation in func.__annotations__.items() if annotation != Any]

def _handle_http_method(method: str):
    """Decorator factory to handle HTTP methods."""
    def decorator(path: str):
        def decorator_inner(func):
            @route(path, method, _require_params(_get_required_params(func)))
            def handler(request):
                return _make_response(func(request))
            return handler
        return decorator_inner
    return decorator

# Decorators for various HTTP methods
def GET(path: str) -> Callable:
    """Decorator for handling GET requests."""
    return _handle_http_method("GET")(path)

def POST(path: str) -> Callable:
    """Decorator for handling POST requests."""
    return _handle_http_method("POST")(path)

def PUT(path: str) -> Callable:
    """Decorator for handling PUT requests."""
    return _handle_http_method("PUT")(path)

def PATCH(path: str) -> Callable:
    """Decorator for handling PATCH requests."""
    return _handle_http_method("PATCH")(path)

def DELETE(path: str) -> Callable:
    """Decorator for handling DELETE requests."""
    return _handle_http_method("DELETE")(path)

def OPTIONS(path: str) -> Callable:
    """Decorator for handling OPTIONS requests."""
    return _handle_http_method("OPTIONS")(path)

def HEAD(path: str) -> Callable:
    """Decorator for handling HEAD requests."""
    return _handle_http_method("HEAD")(path)

def CONNECT(path: str) -> Callable:
    """Decorator for handling CONNECT requests."""
    return _handle_http_method("CONNECT")(path)

def TRACE(path: str) -> Callable:
    """Decorator for handling TRACE requests."""
    return _handle_http_method("TRACE")(path)
