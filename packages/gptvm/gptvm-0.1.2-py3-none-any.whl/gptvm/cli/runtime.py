from concurrent import futures
from typing import Iterable

import grpc
from ..proto import app_pb2, api_pb2_grpc
from ..runner import RemoteRunner, LocalRunner
from ..config import Config

from .import_vm import import_vm

import sys
import io
import pickle
import multiprocessing as mp
import threading

queues = {}

class StdioWrapper(io.TextIOWrapper):
    def __init__(self, file, stdio, q, p):
        super().__init__(stdio)
        self.file = file
        self.stdio = stdio
        self.q = q
        self.p = p

    def write(self, data):
        self.file.write(data)
        self.stdio.write(data)

        self.q.put(self.p(data))

    def flush(self):
        self.file.flush()
        self.stdio.flush()

    def close(self):
        pass

class KeepAliveTimer(object):
    def __init__(self, interval, q):
        self.interval = interval
        self.q = q

        self.start()

    def __del__(self):
        if not self._timer.finished.isSet():
            self._timer.cancel()

    def _run(self):
        self.start()
        self.q.put(app_pb2.RunRemoteRes(heartbeat={}))

    def start(self):
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()

class Worker:
    def __init__(self):
        self.cfg = Config()

    def run(self, app_id, qid, type_, path, fn, args):
        # grpc server has bug to crush with fork mode, so change to spawn
        mpc = mp.get_context('spawn')
        if type_ == app_pb2.FUNCTION:
            q_out = mpc.Queue()
            q_in = mpc.Queue()

            p = mpc.Process(target=self.task_run, args=(self.cfg, q_out, q_in, 0))
            p.start()
        elif type_ == app_pb2.CONSTRUCTOR:
            q_out = mpc.Queue()
            q_in = mpc.Queue()

            qid = id(q_in)
            queues[qid] = q_out, q_in

            p = mpc.Process(target=self.task_run, args=(self.cfg, q_out, q_in, qid))
            p.start()
        else:
            q_out, q_in = queues[qid]

        q_in.put((app_id, type_, path, fn, args))

        while True:
            msg = q_out.get()
            yield msg
            if msg.HasField("ret") or msg.HasField("qid"):
                break

        if type_ == app_pb2.DESTRUCTOR:
            del queues[qid]

    def task_run(self, cfg, q_out, q_in, qid):
        keepalive = KeepAliveTimer(1, q_out)

        objref = None
        while True:
            app_id, type_, path, fn, arguments = q_in.get()

            args, kwargs = pickle.loads(arguments)

            if type_ == app_pb2.FUNCTION or type_ == app_pb2.CONSTRUCTOR:
                runner = RemoteRunner(cfg, '', app_id, False)
                app = import_vm(path)
                # runner = LocalRunner()
                app.attach_runner(runner)

            if type_ == app_pb2.FUNCTION:
                func, _, _ = app.registered_functions[fn]
            elif type_ == app_pb2.CONSTRUCTOR:
                cls, _, _ = app.registered_classes[fn]
                func = cls
            elif type_ == app_pb2.METHOD:
                func = getattr(objref, fn)
                func.obj = objref
            else:
                cls, _, _ = app.registered_classes[fn]
                def empty(obj): pass
                func = cls.__del__ if hasattr(cls, '__del__') else empty
                args = (objref,)

            pack_out = lambda msg: app_pb2.RunRemoteRes(stdout=msg)
            pack_err = lambda msg: app_pb2.RunRemoteRes(stderr=msg)

            tmpio = io.StringIO()
            sys.stdout = StdioWrapper(tmpio, sys.stdout, q_out, pack_out)
            sys.stderr = StdioWrapper(tmpio, sys.stderr, q_out, pack_err)

            try:
                ret = func(*args, *kwargs)
            except BaseException as exc:
                q_out.put(app_pb2.RunRemoteRes(ret=pickle.dumps(exc)))
                break
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

            if type_ == app_pb2.FUNCTION:
                q_out.put(app_pb2.RunRemoteRes(ret=pickle.dumps(ret)))
                keepalive.stop()
                break
            elif type_ == app_pb2.CONSTRUCTOR:
                objref = ret
                q_out.put(app_pb2.RunRemoteRes(qid=qid))
            elif type_ == app_pb2.METHOD:
                q_out.put(app_pb2.RunRemoteRes(ret=pickle.dumps(ret)))
            else:
                q_out.put(app_pb2.RunRemoteRes(qid=0))
                objref = None
                keepalive.stop()
                break

class Runtime(api_pb2_grpc.AppServiceServicer):
    def __init__(self):
        self.worker = Worker()

    def RunRemote(self, request: app_pb2.RunRemoteReq, context) -> Iterable[app_pb2.RunRemoteRes]:
        path, type_ = request.path, request.type
        fn, args = request.fn, request.args
        qid, app_id = request.qid, request.app_id

        return self.worker.run(app_id, qid, type_, path, fn, args)

def runtime():
    port = "50061"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_AppServiceServicer_to_server(Runtime(), server)
    server.add_insecure_port("0.0.0.0:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    runtime()
