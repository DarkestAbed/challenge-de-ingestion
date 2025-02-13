# app/backend/utils/singletons.py
"""
# `Singletons` module
This is a custom implementation of the Singleton class pattern.

Classes:
    Singleton
"""

from typing import Any


class Singleton(type):
    """
    ## `Singleton` class

    Args:
        type (_type_)

    Methods:
        __call__
    """
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        """
        ## Callable instance method

        Returns:
            cls._instances[cls]: _description_ 
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # NOTE: commented else block to enable true singleton and no re-init of the class
        # else:
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
    
    @staticmethod
    def destroy(self):
        cls = self.__class__
        if cls in cls._instances:
            del cls._instances[cls]
