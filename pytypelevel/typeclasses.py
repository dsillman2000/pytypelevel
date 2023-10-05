from typing import Callable, Sequence


class TypeclassMeta(type):

    @classmethod
    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        def __new_instance__(**methods: Callable):
            for k, v in methods.items():
                setattr(cls, k, v)
            return cls
        cls.instance = __new_instance__
