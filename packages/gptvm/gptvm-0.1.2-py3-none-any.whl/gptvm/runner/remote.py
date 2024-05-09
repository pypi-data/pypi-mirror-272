import requests
import sys
import weakref
import os
import inspect
import pickle
import re
import grpc
import tarfile
import glob
import tempfile

from ..api import API
from ..proto import api_pb2_grpc, app_pb2
from ..log import logger

from .base import BaseRunner

class RemoteRunner(BaseRunner):
    def __init__(self, cfg, app_name, app_id = '', is_root = True):
        host = cfg['server']['host']
        port = cfg['server']['port']
        self.api = API(f"{host}:{port}")

        self.is_root = is_root

        # set auth information to api meta data
        if self.is_root:
            token = cfg['default']['token']
        else:
            token = os.environ.get('GPTVM_APP_TOKEN', None)
        self.api_meta = (
            ("authorization", f"Bearer {token}"),
        )

        # set app id
        if self.is_root:
            space_id = cfg['default']['space_id']
            app = self.create_app(app_name, space_id)
            self.app_id = app.id

            self.download_url = self.get_download_url()
        else:
            self.app_id = app_id

        # download app code
        if not self.is_root:
            self.download_app_code()

        # set local test runtime address
        self.test_addr = os.environ.get('RUNTIME_TEST_URL', None)

    def __del__(self):
        if self.is_root:
            self.stop_app()

    def function_setup(self, func, *args, **kwargs):
        pass

    def function_create(self, func, *args, **kwargs):
        print(">>>", args, kwargs)
        task = self.create_task(func.__name__, *args, **kwargs)
        weakref.finalize(self, self.delete_task, task.name, task.suid)

        func.task = task

    def function_call(self, func, *args, **kwargs):
        task = func.task

        return self.run_task(task.addr, app_pb2.FUNCTION, func, 0, *args, **kwargs)

    def class_setup(self, cls, *args, **kwargs):
        pass

    def class_create(self, cls, *args, **kwargs):
        print(">>>", args, kwargs)
        task = self.create_task(cls.__name__, *args, **kwargs)
        weakref.finalize(self, self.delete_task, task.name, task.suid)

        # remove destructor on local
        if hasattr(cls, '__del__'):
            delattr(cls, '__del__')

        cls.task = task
        pass

    def class_object_new(self, cls, *args, **kwargs):
        task = cls.task

        qid = self.run_task(task.addr, app_pb2.CONSTRUCTOR, cls, 0, *args, **kwargs)

        obj = cls.__new__(cls)
        obj.task = task
        obj.qid = qid

        # remove remote ref while self deleted or program exit
        weakref.finalize(obj, self.run_task, task.addr, app_pb2.DESTRUCTOR, cls, qid)

        return obj

    def class_object_call_method(self, method, obj, *args, **kwargs):
        task = obj.task

        return self.run_task(task.addr, app_pb2.METHOD, method, obj.qid, *args, **kwargs)

    # ======

    def create_app(self, name, workspace_id):
        app: api_pb2_grpc.AppServiceStub = self.api.app

        res = app.Create(
            app_pb2.CreateReq(
                name=name,
                workspace_id=workspace_id,
            ),
            metadata=self.api_meta
        )
        if res.code != 0:
            raise RuntimeError("App {name} create failed: " + res.msg)

        logger.info(f"App {res.app.name} created.")

        fd, tmp_fn = tempfile.mkstemp()
        os.close(fd)

        with tarfile.open(tmp_fn, "w|gz") as tar:
            for name in glob.glob('**/*.py', recursive=True):
                tar.add(name)
                logger.debug(f" - {name} mounted.")

        logger.info(f'App upload url: {res.upload_url}')
        with open(tmp_fn, 'rb') as f:
            r = requests.put(res.upload_url, data=f)
            r.raise_for_status()

        logger.info(f"App {res.app.name} mounted.")

        return res.app

    def get_download_url(self):
        app: api_pb2_grpc.AppServiceStub = self.api.app

        res: app_pb2.UrlRes = app.GetPackageUrl(
            app_pb2.UrlReq(
                id=self.app_id,
                type=app_pb2.DOWNLOAD,
            ),
            metadata=self.api_meta
        )

        logger.info(f'App download url: {res.download_url}')
        return res.download_url

    def download_app_code(self):
        url = os.environ.get('GPTVM_APP_CODE_URL', None)

        logger.info(f'App download url: {url}')

        fd, tmp_fn = tempfile.mkstemp()
        os.close(fd)

        with open(tmp_fn, 'wb') as f:
            r = requests.get(url)
            f.write(r.content)
            r.raise_for_status()

        with tarfile.open(tmp_fn, "r|gz") as tar:
            tar.extractall()

        logger.info(f"App code extracted.")

    def stop_app(self):
        app: api_pb2_grpc.AppServiceStub = self.api.app

        res = app.Stop(
            app_pb2.StopReq(
                id=self.app_id,
            ),
            metadata=self.api_meta,
        )
        if res.code != 0:
            raise RuntimeError("App stop failed: " + res.msg)

        if sys.meta_path:
            logger.info(f"App stoped.")

    def create_task(self, name, *args, **kwargs):
        logger.debug(f"Task create: {name}.")
        app: api_pb2_grpc.AppServiceStub = self.api.app

        resources=[]

        gpu = kwargs.pop("gpu", None)
        if gpu is not None:
            if gpu == 'any':
                gpu = 1
            r = app_pb2.TaskResource(type='gpu', quantity=str(gpu))
            resources.append(r)

        res = app.Operate(
            app_pb2.OperateReq(
                id=self.app_id,
                action=app_pb2.START,
                task=app_pb2.TaskRequest(
                    name=name.lower(),
                    image="harbor.gptvm.ai/gptvm/runtime-vllm",
                    code_location=self.download_url,
                    resources=resources,
                ),
            ),
            metadata=self.api_meta,
        )
        if res.code != 0:
            raise RuntimeError("Task create failed: {name}, " + res.msg)

        logger.debug(f"Task started: {name}.")

        return res.task

    def delete_task(self, name, suid):
        app: api_pb2_grpc.AppServiceStub = self.api.app

        res = app.Operate(
            app_pb2.OperateReq(
                id=self.app_id,
                action=app_pb2.STOP,
                task=app_pb2.TaskRequest(
                    name=name,
                    suid=suid,
                ),
            ),
            metadata=self.api_meta,
        )
        if res.code != 0:
            raise RuntimeError("Task remove failed: {name}, " + res.msg)

        logger.debug(f"Task stoped: {name}.")

        return res.task

    def run_task(self, addr, mtype, func, qid, *args, **kwargs):
        addr = self.test_addr if self.test_addr else addr

        addr = re.sub(r'^([^.]*)\.', r'\1-grpc.', addr)
        if ':' not in addr:
            addr = addr + ':80'
        api = API(addr)

        app: api_pb2_grpc.AppServiceStub = api.app

        args = pickle.dumps((args, kwargs))

        path = os.path.relpath(inspect.getfile(func))
        if hasattr(func, 'orig_path'):
            path = os.path.relpath(func.orig_path)

        while True:
            try:
                res_iter = app.RunRemote(
                    app_pb2.RunRemoteReq(
                        path=path, fn=func.__name__, args=args,
                        type=mtype, qid=qid,
                        addr=addr,
                        app_id=self.app_id,
                    ),
                    metadata=self.api_meta,
                    wait_for_ready=True,
                )

                for res in res_iter:
                    if res.HasField("stdout"):
                        sys.stdout.write(res.stdout)
                    elif res.HasField("stderr"):
                        sys.stderr.write(res.stderr)
                    elif res.HasField("ret"):
                        ret = pickle.loads(res.ret)
                        if isinstance(ret, BaseException):
                            raise ret
                    elif res.HasField("qid"):
                        ret = res.qid
                    elif res.HasField("heartbeat"):
                        pass
                    else:
                        raise RuntimeError(
                            "Received invalid RunResponse."
                        )
                break
            except grpc.RpcError as e:
                # wait to connect next task
                if e.code() == grpc.StatusCode.UNIMPLEMENTED:
                    continue
                if e.code() == grpc.StatusCode.UNKNOWN:
                    continue
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    continue
                raise e

        return ret
