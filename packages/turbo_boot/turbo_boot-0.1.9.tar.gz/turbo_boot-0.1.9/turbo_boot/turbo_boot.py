import inspect
import os
from importlib import import_module
from typing import Dict, Optional

from fastapi import FastAPI

from turbo_boot.logging import Logger

Any = object()


def convert_filename_to_classname(filename):
    if "_" in filename:
        words = filename.split("_")
        capitalized_words = [word.capitalize() for word in words]
        class_name = "".join(capitalized_words)
        return class_name
    return filename


def build_application(application_path: str, fast_api_app_configs: Optional[Dict] = None):
    if application_path is None:
        raise ValueError("application_path can not be None")

    arguments_to_remove = ["self"]
    argument_list = list(inspect.signature(FastAPI.__init__).parameters.keys())
    filtered_arguments = [arg for arg in argument_list if arg not in arguments_to_remove]
    parameters = {}
    for argument in filtered_arguments:
        if argument in fast_api_app_configs:
            parameters[argument] = fast_api_app_configs[argument]
    app = FastAPI(**parameters)

    for root, dirs, files in os.walk(application_path):
        for file in files:
            if (
                file.endswith(".py")
                and not file.startswith("__")
                and file != "main.py"
                and "alembic" not in root
                and "exceptions" not in root
                and "usecase" not in root
            ):
                module_name = os.path.relpath(os.path.join(root, file), application_path)
                module_name = module_name.replace(os.path.sep, ".")[:-3]

                try:
                    module = import_module(module_name)
                    class_info = {key: value for key, value in inspect.getmembers(module, inspect.isclass)}
                    class_name = convert_filename_to_classname(module_name.split(".")[-1])

                    if class_name in class_info.keys():
                        if "__api_router__" in class_info[class_name].__dict__.keys():
                            app.include_router(class_info[class_name].__dict__["__api_router__"])
                except ImportError as e:
                    print(f"Error loading module '{module_name}': {e}")

    return app


def get_logger(config_loader) -> Logger:
    
    logger = Logger(config_loader)

    return logger


class TurboBoot:
    logger = None
    app = None
    
    @staticmethod
    def setup(application_path: str = None, fast_api_app_configs: Optional[Dict] = None):
        if application_path is None or len(application_path.strip()) < 1:
            raise ValueError("application_path can be None or empty")
        
        TurboBoot.app = build_application(application_path, fast_api_app_configs)

    @staticmethod
    def get_app():
        return TurboBoot.app
