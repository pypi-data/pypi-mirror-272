# Copyright gptvm.ai 2024

import typer

from .import_vm import import_vm

from ..runner import LocalRunner, RemoteRunner
from ..config import Config
from ..log import logger_set_debug

serve_typer = typer.Typer()

path_help_str = '''
Path to the python file, \n
use `{file}::{serve},...` to specify serves to run, otherwise run all one-by-one.
'''

@serve_typer.command()
def launch(
    is_local: bool = typer.Option(False, "--local", "-l", help="Run app on local machine for debugging"),
    path: str = typer.Argument(
        ...,
        help=path_help_str,
    ),
):
    file, *serves = path.split('::')

    logger_set_debug()

    app = import_vm(file)

    if len(app.registered_serves) == 0:
        raise RuntimeError(f"No serve found, skip.")
    
    # attach api to create app
    cfg = Config()

    runner = LocalRunner() if is_local else RemoteRunner(cfg, app.name)
    app.attach_runner(runner)

    # run serves one-by-one
    if len(serves) != 0:
        for sv in serves[0].split(','):
            if sv not in app.registered_serves:
                raise RuntimeError(f"Invalid serve name: {sv}.")

            app.run_web_serve(sv)
    else:
        for sv in app.registered_serves:
            app.run_web_serve(sv)


@serve_typer.command()
def stop(
    file: str = typer.Argument(..., help="Path to the python file"),
    name: list[str] = typer.Option(None, help="Names of the serve to stop"),
):
    vm = import_vm(file)

    # if user doesn't provide the serve to stop, bring up the list of running serve
    if len(name) == 0:
        print("Stop serve:")
        for k in vm._registered_serve.keys():
            print(k)
            vm.stop_serve(k)
    else:
        for n in name:
            vm.stop_serve(n)


@serve_typer.command()
def list(
    file: str = typer.Argument(..., help="Path to the python file"),
):
    vm = import_vm(file)

    print("Available serve:")
    for k in vm.registered_serve.keys():
        print(k)

    print("Running serve:")
    for k in vm.running_serve:
        print(k)
