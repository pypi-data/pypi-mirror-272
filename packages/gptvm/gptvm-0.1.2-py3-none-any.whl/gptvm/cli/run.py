# Copyright gptvm.ai 2024

import typer

from .import_vm import import_vm

from ..runner import LocalRunner, RemoteRunner
from ..config import Config
from ..log import logger_set_debug

path_help_str = '''
Path to the python file, \n
use `{file}::{entrypoint},...` to specify entrypoints to run, otherwise run all one-by-one.
'''

def run_cli(
    is_local: bool = typer.Option(False, "--local", "-l", help="Run app on local machine for debugging"),
    path: str = typer.Argument(
        ...,
        help=path_help_str,
    ),
):
    file, *entrypoints = path.split('::')

    logger_set_debug()

    app = import_vm(file)

    if len(app.registered_local_entrypoints) == 0:
        raise RuntimeError(f"No local entrypoint found, skip.")

    # attach api to create app
    cfg = Config()

    runner = LocalRunner() if is_local else RemoteRunner(cfg, app.name)
    app.attach_runner(runner)

    # run entrypoints one-by-one
    if len(entrypoints) != 0:
        for ep in entrypoints[0].split(','):
            if ep not in app.registered_local_entrypoints:
                raise RuntimeError(f"Invalid entrypoint name: {ep}.")

            app.run_local_entrypoint(ep)
    else:
        for ep in app.registered_local_entrypoints:
            app.run_local_entrypoint(ep)