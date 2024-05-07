from functools import wraps


def validate_path(path: str):
    if path is None or len(path.strip()) < 1:
        raise ValueError("Path cannot be None or empty")

    if path is not None:
        if not path.startswith("/"):
            raise ValueError("Path must start with '/'")


def GetMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "GET", "path": path, **kwargs}
        return wrapper

    return decorator


def PostMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "POST", "path": path, **kwargs}
        return wrapper

    return decorator


def PutMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "PUT", "path": path, **kwargs}
        return wrapper

    return decorator


def DeleteMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "DELETE", "path": path, **kwargs}
        return wrapper

    return decorator


def OptionsMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "OPTIONS", "path": path, **kwargs}
        return wrapper

    return decorator


def HeadMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "HEAD", "path": path, **kwargs}
        return wrapper

    return decorator


def PatchMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "PATCH", "path": path, **kwargs}
        return wrapper

    return decorator


def TraceMapping(path: str, **kwargs):
    validate_path(path=path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__metadata__ = {"method_name": "TRACE", "path": path, **kwargs}
        return wrapper

    return decorator
