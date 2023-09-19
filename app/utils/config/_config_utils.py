import os
from typing import Any
import inspect

class Field:
    def __init__(self, env_name: str | None = None):
        self.env_name = env_name
    
    def get_value(self, prefix: str, default_env_name: str, envs: list) -> Any | None:
        env_full_name = \
            f'{prefix}{self.env_name if self.env_name else default_env_name}'
        return envs[env_full_name] if env_full_name in envs else None


def _config_repr(class_, env_values: list = [], prefix: str | None = None):
    prefix = f'{prefix}__' if prefix else ''
    for i in inspect.getmembers(class_):
        if i[0].startswith('__'):
            continue
        if hasattr(i[1], 'get_value'):
            # is field
            new_attr_value = i[1].get_value(prefix, i[0], env_values)
            setattr(class_, i[0], new_attr_value)
        else:
            # is class
            _config_repr(i[1], env_values, f'{prefix}{i[1].__configname__}')
    return class_


def config_repr(class_=None, *, 
                env_values: list | None = None):
    if not class_:
        def wrapper(class_):
            return _config_repr(class_, env_values if env_values else os.environ)
        return wrapper
    else:
        return _config_repr(class_, os.environ)
    

def config_sub(class_=None, *, config_name: str | None = None):
    if not class_:
        def wrapper(class_):
            if config_name:
                setattr(class_, '__configname__', config_name)
            elif not hasattr(class_, '__configname__'):
                setattr(class_, '__configname__', class_.__name__)
            return class_
        return wrapper
    else:
        if config_name:
            setattr(class_, '__configname__', config_name)
        elif not hasattr(class_, '__configname__'):
            setattr(class_, '__configname__', class_.__name__)
        return class_    
    
    
# if __name__ == '__main__':
#     print(Configs.JWT.SECRET_KEY)
#     print(Configs.NEO4J.DEFAULT.USER)
#     print(Configs.NEO4J.TEST.USER)
    
    