class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ObjectUtil:

    @classmethod
    def is_null(cls, obj):
        return obj is None

    @classmethod
    def is_not_null(cls, obj):
        return not cls.is_null(obj)
