# import ray

from .log import logger


class Cls(object):
    def __init__(self):
        logger.debug("Initializing Cls")
        cls_local = getattr(self, "cls_local", None)
        if cls_local is not None:
            self.cls_vm = ray.remote(num_gpus=1, lifetime="detached")(
                cls_local
            ).remote()
            for method in dir(cls_local):
                # check if the method is a function
                if callable(getattr(cls_local, method)) and not method.startswith("__"):
                    # create the method
                    real_method = _Method(getattr(cls_local, method), self.cls_vm)
                    # register the method
                    setattr(self, method, real_method)
                    logger.debug(f"Registered method: {real_method}")
        logger.debug(f"Cls initialized: {self.cls_vm}")


# Class used to abstract the method of the original class
class _Method(object):
    def __init__(self, func, cls_vm):
        self.func_local = func
        self.name = func.__name__
        self.cls_vm = cls_vm

    def __call__(self, *args, **kwargs):
        pass

    def remote(self, *args, **kwargs):
        logger.debug(f"Calling method: {self.name}")
        self.func_remote = getattr(self.cls_vm, self.name)
        return ray.get(self.func_remote.remote(*args, **kwargs))
