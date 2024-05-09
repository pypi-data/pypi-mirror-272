import abc

class BaseRunner(abc.ABC):
    def function_setup(self, func, *args, **kwargs):
        raise NotImplementedError()

    def function_create(self, func, *args, **kwargs):
        raise NotImplementedError()

    def function_call(self, func, *args, **kwargs):
        raise NotImplementedError()

    def class_setup(self, cls, *args, **kwargs):
        raise NotImplementedError()

    def class_create(self, cls, *args, **kwargs):
        raise NotImplementedError()

    def class_object_new(self, cls, *args, **kwargs):
        raise NotImplementedError()

    def class_object_call_method(self, method, obj, *args, **kwargs):
        raise NotImplementedError()