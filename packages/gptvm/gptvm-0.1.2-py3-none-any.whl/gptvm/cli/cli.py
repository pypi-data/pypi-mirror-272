# Copyright gptvm.ai 2024

import typer

from .auth import login_cli, logout_cli
from .run import run_cli
from .app import app_typer
from .env import env_typer
from .serve import serve_typer
from .runtime import runtime

# define the command line entry point
cli_typer = typer.Typer(pretty_exceptions_enable=False)


@cli_typer.callback(invoke_without_command=True)
def version(
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
):
    pass

@cli_typer.callback(invoke_without_command=True)
def debugger(
    debugger: bool = typer.Option(False, "--debugger", "-d", help="Run with python debugger"),
):
    if debugger:
        import debugpy

        debugpy.listen(5678)
        print("Waiting for debugger attach...")
        debugpy.wait_for_client()
        print("Python debugger attached.")
        debugpy.breakpoint()

cli_typer.command("run", help="Run an app with local entrypoints.", no_args_is_help=True,
                  context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(
    run_cli
)

cli_typer.add_typer(app_typer, name="app", help="Manage the applications")
cli_typer.add_typer(env_typer, name="env", help="Manage the environments and variables")
cli_typer.add_typer(serve_typer, name="serve", help="Manage the serve")

cli_typer.command("login", help="login to gptvm.ai")(login_cli)
cli_typer.command("logout", help="logout from gptvm.ai")(logout_cli)

cli_typer.command("runtime", hidden=True)(runtime)

if __name__ == "__main__":
    cli_typer()
