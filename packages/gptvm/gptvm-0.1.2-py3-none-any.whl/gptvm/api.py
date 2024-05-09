import grpc
from .proto import api_pb2_grpc

class API:
    def __init__(self, addr = "localhost:5000"):
        channel = grpc.insecure_channel(addr)

        self.app = api_pb2_grpc.AppServiceStub(channel)
        self.user = api_pb2_grpc.UserServiceStub(channel)
        self.env = api_pb2_grpc.EnvServiceStub(channel)

        self.channel = channel

    def __del__(self):
        self.channel.close()