import inspect
from typing import Dict, Optional, Type

from fastapi import APIRouter


class RestController:
    def __init__(self, prefix: Optional[str] = None, dependencies: Optional[Dict] = None):
        self.prefix = prefix
        if prefix is not None:
            if prefix == "/":
                raise ValueError("Prefix cannot be '/'")
            if not prefix.startswith("/"):
                raise ValueError("Prefix must start with '/'")
        self.dependencies = dependencies

    def __call__(self, cls: Type) -> Type:
        setattr(cls, "__rest_controller__", True)

        router = APIRouter()
        setattr(cls, "__api_router__", router)

        instance = cls(**(self.dependencies or {}))

        for attr_name in dir(cls):
            attr_value = getattr(instance, attr_name)
            if callable(attr_value) and not attr_name.startswith("__"):
                if hasattr(attr_value, "__metadata__"):
                    arguments_to_remove = ["self", "path", "methods", "endpoint"]
                    argument_list = list(inspect.signature(APIRouter.add_api_route).parameters.keys())
                    filtered_arguments = [arg for arg in argument_list if arg not in arguments_to_remove]
                    parameters = {}
                    parameters["methods"] = [attr_value.__metadata__.get("method_name")]
                    if self.prefix is not None:
                        m_prefix = self.prefix.rstrip("/")
                        m_path = attr_value.__metadata__["path"].rstrip("/")
                        m_path = m_path.lstrip("/")
                        if len(m_path) > 0:
                            parameters["path"] = m_prefix + "/" + m_path
                        else:
                            parameters["path"] = m_prefix
                    else:
                        parameters["path"] = attr_value.__metadata__["path"]

                    parameters["endpoint"] = attr_value

                    for argument in filtered_arguments:
                        if argument in attr_value.__metadata__:
                            parameters[argument] = attr_value.__metadata__[argument]

                    router.add_api_route(**parameters)

        return cls
