import random
from typing import Generator, List


def dict_field_values(fields: list, values: List[Generator]):
    return [dict(zip(fields, _)) for _ in values]


def dict_merge_update(result_dict, update_dict):
    for k, v in update_dict.items():
        if k not in result_dict:
            result_dict[k] = v
        else:
            result_dict[k] += v


def get_random_str(length: int = 6, str_type: int = 0) -> str:
    """
    :param length: Returned string length
    :param str_type: Returned string type, 0: Numbers and letters, 1: Only numbers, 2: Only letters
    :return: str
    """
    if str_type == 1:
        return ''.join(random.sample('0123456789', length))
    elif str_type == 2:
        return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', length))
    else:
        return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', length))
