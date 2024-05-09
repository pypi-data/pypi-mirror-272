from .base import BaseRunner

class LocalRunner(BaseRunner):
    def function_setup(self, func, *args, **kwargs):
        pass

    def function_create(self, func, *args, **kwargs):
        pass

    def function_call(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    def class_setup(self, cls, *args, **kwargs):
        pass

    def class_create(self, cls, *args, **kwargs):
        pass

    def class_object_new(self, cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def class_object_call_method(self, method, obj, *args, **kwargs):
        return method(obj, *args, **kwargs)