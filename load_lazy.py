import json
import logging
import os
import sys
import types


logger = logging.getLogger()


# class LoadLazy(object):
#
#     def __init__(self):
#         pass
#
#     def __call__(self, original_function):
#         @wraps(original_function)
#         def lazy_function(*args, **kwargs):
#             return Proxy(lambda: original_function(*args, **kwargs))
#         print("in __call__ getcwd()->", os.getcwd())
#
#         return lazy_function


class LoadLazy:

    def __init__(self, func):
        self.func = func

    def __getattr__(self, key):
        if key not in self.__dict__:
            self.__dict__[key] = self.func()[key]

        return self.__dict__[key]


@LoadLazy
def extract_metadata(file_name='.build.json'):
    """Reads a JSON file located in the same directory as 'setup.py' and returns
     the data in it as a dictionary."""

    file_path = os.path.dirname(os.path.realpath(__file__)) + '/' + file_name
    try:
        with open(file_path) as file:
            metadata = json.loads(file.read())

    except FileNotFoundError as e:
        logger.warning(f"There was no '{e.filename}' file found!")
        return {}
    except json.JSONDecodeError as e:
        logger.warning(f"There was a JSONDecodeError: \n'{e.args[0]}'")
        return {}

    return metadata


# class GetAttr(type):
#     def __getitem__(cls, x):
#         return getattr(cls, x)
#
# class Fruit(object):
#     __metaclass__ = GetAttr
#
#     Apple = 0
#     Pear = 1
#     Banana = 2
#
# print Fruit['Apple'], Fruit['Banana']

