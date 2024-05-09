# vm define a virtual execution environment for the program

import os

from .log import logger
from .config import Config
from .runner import BaseRunner

class App(object):

    def __init__(self, name):
        logger.debug("Initializing App: %s", name)
        self.name = name
        self.config = Config()

        self._registered_classes = {}
        self._registered_methods = {}
        self._registered_functions = {}
        self._registered_serves = {}
        self._registered_local_entrypoints = {}

        self.remote_disabled = os.environ.get('GPTVM_DISABLE_REMOTE', 0)
        self._runner: BaseRunner = None

    @property
    def runner(self):
        if self._runner is None:
            raise RuntimeError("Runner is not attached.")

        return self._runner

    def attach_runner(self, runner: BaseRunner):
        for func, args, kwargs in self.registered_functions.values():
            runner.function_setup(func, *args, **kwargs)

        for cls, args, kwargs in self.registered_classes.values():
            runner.class_setup(cls, *args, **kwargs)

        self._runner = runner

    def __del__(self):
        pass

    # querry the registered functions
    @property
    def registered_functions(self):
        logger.debug("Querrying registered functions")
        return self._registered_functions

    # querry the registered classes
    @property
    def registered_classes(self):
        logger.debug("Querrying registered classes")
        return self._registered_classes

    @property
    def registered_serves(self):
        logger.debug("Querrying registered serve")
        return self._registered_serves

    @property
    def registered_local_entrypoints(self):
        logger.debug("Querrying registered entrypoints")
        return self._registered_local_entrypoints

    # Decorator to register a new function with this VM
    def function(self, name = None, *args, **kwargs):
        def decorator(func):
            func_name = name
            if func_name is None:
                func_name = func.__name__
            logger.debug(f"Registering function: {func_name}")
            self._registered_functions[func_name] = (func, args, kwargs,)

            def _remote(*args_r, **kwargs_r):
                self.runner.function_create(func, *args, **kwargs)
                # call function on remote
                return self.runner.function_call(func, *args_r, **kwargs_r)

            def _map(iter, *iters):
                return map(_remote, iter, *iters)

            def _starmap(args_iter, kwargs_iter = None):
                if kwargs_iter is not None:
                    for args, kwargs in zip(args_iter, kwargs_iter):
                        yield _remote(*args, **kwargs)
                else:
                    for args in args_iter:
                        yield _remote(*args)

            func.remote = _remote
            func.map = _map
            func.starmap = _starmap

            logger.debug("Remote function created: %s", func_name)
            return func

        return decorator


    # Decorator to register a new class with this VM
    def cls(self, name = None, *args, **kwargs):

        def decorator(cls):
            cls_name = name
            if cls_name is None:
                cls_name = cls.__name__
            logger.debug("Registering class: %s", cls_name)
            self._registered_classes[cls_name] = (cls, args, kwargs,)

            # define method wrapper for remote
            class MethodWrapper(object):
                def __init__(mself, method):
                    mself.obj = None
                    mself.method = method

                def __call__(mself, *args, **kwargs):
                    # call method on local
                    return mself.method(mself.obj, *args, **kwargs)

                def remote(mself, *args, **kwargs):
                    # call method on remote
                    return self.runner.class_object_call_method(mself.method, mself.obj, *args, **kwargs)

            # attach method wrappers for remote
            for m in dir(cls):
                # check if the method is a function
                if callable(getattr(cls, m)) and not m.startswith("__") and m != "remote":
                    method = getattr(cls, m)
                    setattr(cls, m, MethodWrapper(method))

            @classmethod
            def remote(cls, *args_r, **kwargs_r):
                logger.debug(f"Remote class constructor: {cls_name}, {cls.__module__}")

                self.runner.class_create(cls, *args, **kwargs)

                # created local stub for obj
                obj = self.runner.class_object_new(cls, *args_r, **kwargs_r)

                for method in dir(obj):
                    # check if the method is a function
                    if callable(getattr(obj, method)) and not method.startswith("__") and method != "remote":
                        m = getattr(obj, method)
                        m.obj = obj

                return obj

            cls.remote = remote

            logger.info(f"Remote class created: {cls.__name__}")
            return cls

        return decorator

    # Decorator the local entrypoints to run the program
    def local_entrypoint(
        self,
        name=None,
    ):
        def decorator(func, name=name):
            if name is None:
                name = func.__name__
            logger.debug("Registering local entrypoint: %s", name)

            self._registered_local_entrypoints[name] = func
            return func

        return decorator

    def serve_function(self, name = None, port = 80, *args, **kwargs):
        def decorator(func, name=name):
            if name is None:
                name = func.__name__
            logger.debug("Registering endpoint: /%s", name)

            def serve():
                import uvicorn, fastapi

                api = fastapi.FastAPI()
                api.get(f"/{name}")(func)
                uvicorn.run(api, host="0.0.0.0", port=port)

            serve.__name__ = func.__name__
            serve.__module__ = func.__module__
            serve.__doc__ = func.__doc__
            serve.orig_path = func.__code__.co_filename

            if name in self._registered_functions:
                raise RuntimeError(f"@app.function should be placed before @app.web_endpoint: {name}")

            self._registered_serves[func.__name__] = serve

            return serve

        return decorator

    def serve_fastapi(self, name = None, port = 8000, *args, **kwargs):
        def decorator(func, name=name):
            if name is None:
                name = func.__name__
            logger.debug("Registering endpoint: /%s", name)

            def serve():
                import uvicorn, fastapi

                api = fastapi.FastAPI()
                func(api)
                uvicorn.run(api, host="0.0.0.0", port=port)

            serve.__name__ = func.__name__
            serve.__module__ = func.__module__
            serve.__doc__ = func.__doc__
            serve.orig_path = func.__code__.co_filename

            if name in self._registered_functions:
                raise RuntimeError(f"@app.function should be placed before @app.web_endpoint: {name}")

            self._registered_serves[func.__name__] = serve

            return serve

        return decorator

    def run_local_entrypoint(self, ep):
        logger.debug(f'Run local entrypoint: {ep}.')

        self._registered_local_entrypoints[ep]()
    
    def run_web_serve(self, sv):
        logger.debug(f'Run serve: {sv}.')

        self._registered_functions[sv][0].remote()