# Copyright gptvm.ai 2024

import typer
from typing_extensions import Annotated

from ..api import API
from ..config import Config
from ..proto import api_pb2_grpc, user_pb2, env_pb2

env_typer = typer.Typer()

@env_typer.command(help="Create a new environment variable")
def create(
    key: Annotated[str, typer.Argument(help="Name of the environment variable <Unique>")],
    value: Annotated[str, typer.Argument(help="Value of environment variable")],
    is_secret: Annotated[bool, typer.Argument(help="Is a secret")] = False,
):
    print(f"Creating env: {key}: {value}")

    cfg = Config()

    host = cfg['server']['host']
    port = cfg['server']['port']
    api = API(f"{host}:{port}")

    env: api_pb2_grpc.EnvServiceStub = api.env

    token = Config()['default']['token']

    api_meta = (
        ("authorization", f"Bearer {token}"),
    )

    res: env_pb2.CreateRes = env.Create(env_pb2.CreateReq(name=key, value=value, is_secret=is_secret), metadata=api_meta)
    print(res)
    


@env_typer.command(help="Delete an exist environment variable")
def delete(name: str):
    print(f"Deleting env: {name}")
