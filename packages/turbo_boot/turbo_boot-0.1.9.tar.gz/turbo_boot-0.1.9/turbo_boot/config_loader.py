import os

import yaml

from turbo_boot.singleton_meta import SingletonMeta

def get_config_file_path():
    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    if os.environ.get('ENVIRONMENT') == 'TEST':
        return os.path.join(dir_path, 'tests', 'resources', 'application.yaml')
    else:
        return os.path.join(dir_path, 'src', 'resources', 'application.yaml')
    pass
    
class ConfigLoader(metaclass=SingletonMeta):
    def __init__(self, config_file_path: str = get_config_file_path()) -> None:
        self.__yaml_data = None
        self.config_file = config_file_path
        self.__load_config()

    def __load_config(self):
        with open(self.config_file, "r") as yaml_file:
            self.__yaml_data = yaml.safe_load(yaml_file)

    def get_config(self, key: str):
        return self.__get_yaml_value_with_env_substitution(self.__yaml_data, key)

    def __get_yaml_value_with_env_substitution(self, yaml_data, path):
        keys = path.split(".")
        value = yaml_data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, None)
                if value is None:
                    return None
            else:
                return None
        return self.__substitute_env_variables(value)

    def __substitute_env_variables(self, value):
        if isinstance(value, str):
            parts = value.split(":$")
            if len(parts) == 2 and parts[1].startswith("{") and parts[1].endswith("}"):
                env_var = parts[1][2:-1]
                return os.environ.get(env_var, parts[0])
        return value