# Copyright gptvm.ai 2024

import typer

from ..api import API
from ..config import Config
from ..proto import api_pb2_grpc, user_pb2

def login_cli():
    email = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True)

    cfg = Config()

    host = cfg['server']['host']
    port = cfg['server']['port']
    api = API(f"{host}:{port}")

    user: api_pb2_grpc.UserServiceStub = api.user

    res = user.Login(user_pb2.LoginReq(email=email, password=password))
    print(res)
    cfg['default']['user'] = res.user_info.username
    cfg['default']['token'] = res.token
    cfg['default']['space_id'] = res.default_space.id
    cfg['default']['group_id'] = res.default_group.id
    cfg.save()

    print('login success.')

def logout_cli():
    config = Config()

    config.remove()

    print('logout success.')
