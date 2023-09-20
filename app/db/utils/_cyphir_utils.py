from typing import Tuple


def cyphir_list_formatter(keys: list, center: str, 
                     left: str = '{}', 
                     right: str = '{}',
                     around: Tuple[str, str] = ('', '')) -> str:
    result = f'{around[0]} '
    result += ', '.join([f'{left} {center} {right}'.format(k, k) for k in keys])
    result += f'{around[1]}'
    return result

def compile_cyphir_list_formatter(center: str, left: str = '{}', right: str = '{}',
                             around: Tuple[str, str] = ('', '')):
    def wrapper(key_values: dict):
        _key_values = {k: v for k, v in key_values.items() if v is not None}
        return cyphir_list_formatter(_key_values.keys(), center, left, right, around)
    return wrapper

def cyphir_dict_formatter(key_values: dict, center: str,
                     left: str = '{}', 
                     right: str = '{}',
                     around: Tuple[str, str] = ('', '')) -> str:
    result = f'{around[0]} '
    result += ', '.join([f'{left} {center} {right}'.format(k, v.__repr__) for k, v in key_values.items()])
    result += f'{around[1]}'
    return result

def compile_cyphir_dict_formatter(center: str, left: str = '{}', right: str = '{}',
                             around: Tuple[str, str] = ('', '')):
    def wrapper(key_values: dict):
        _key_values = {k: v for k, v in key_values.items() if v is not None}
        return cyphir_dict_formatter(_key_values, center, left, right, around)
    return wrapper

