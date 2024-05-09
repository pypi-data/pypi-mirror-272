# Copyright gptvm.ai 2024

import typer
from datetime import timezone, datetime

from rich.console import Console
from rich.table import Table

from ..api import API
from ..config import Config
from ..proto import api_pb2_grpc, app_pb2

status_map = {
    app_pb2.AppState.CREATED: "[grey66]Created :white_circle:",
    app_pb2.AppState.STARTING: "[bright_cyan]Starting :blue_circle:",
    app_pb2.AppState.QUEUED: "[bright_blue]Queued :purple_circle:",
    app_pb2.AppState.RUNNING: "[green]Running :green_circle:",
    app_pb2.AppState.STOPPED: "[yellow]Stopped :brown_circle:",
}

app_typer = typer.Typer()

@app_typer.command(help="List applications.")
def list():
    cfg = Config()

    host = cfg['server']['host']
    port = cfg['server']['port']
    api = API(f"{host}:{port}")

    app: api_pb2_grpc.AppServiceStub = api.app

    cfg = Config()
    token = cfg['default']['token']

    api_meta = (
        ("authorization", f"Bearer {token}"),
    )

    res: app_pb2.ListRes = app.List(app_pb2.ListReq(workspace_id=cfg['default']['space_id']), metadata=api_meta)

    console = Console()

    from rich import box

    table = Table(
        show_edge=False,
        show_header=True,
        expand=False,
        row_styles=["none", "dim"],
        box=box.SIMPLE,
    )
    table.add_column("[green]Name", style="green", no_wrap=True)
    table.add_column("Unique ID")
    table.add_column(
        "[gray]Status :white_circle:",
        style="green",
        justify="right",
        no_wrap=True,
    )
    table.add_column(
        "[cyan]Start Time",
        style="cyan",
        justify="right",
        no_wrap=True,
    )
    table.add_column(
        "[magenta]Run Time",
        style="magenta",
        justify="right",
        no_wrap=True,
    )

    for app in res.apps[:10]:
        start_time = app.created_at.ToDatetime(tzinfo=timezone.utc).astimezone()
        end_time = app.updated_at.ToDatetime(tzinfo=timezone.utc).astimezone()
        if app.status != app_pb2.AppState.STOPPED and app.status != app_pb2.AppState.CREATED:
            end_time = datetime.now(timezone.utc)

        table.add_row(
            app.name,
            app.suid,
            status_map[app.status],
            start_time.strftime("%Y-%m-%d %H:%M:%S.%f %Z"),
            str(end_time - start_time)
        )

    console.print(table)


@app_typer.command(help="Display an application information.")
def info(suid: str):
    cfg = Config()

    host = cfg['server']['host']
    port = cfg['server']['port']
    api = API(f"{host}:{port}")

    app: api_pb2_grpc.AppServiceStub = api.app

    token = Config()['default']['token']

    api_meta = (
        ("authorization", f"Bearer {token}"),
    )

    res: app_pb2.InfoRes = app.Info(app_pb2.InfoReq(suid=suid), metadata=api_meta)

    console = Console()

    table = Table.grid(padding=(0, 2), pad_edge=True)
    table.add_column("Key", no_wrap=True, justify="right", style="bold red")
    table.add_column("Value")

    table.add_row("Name", res.app.name)
    table.add_row("Unique ID", res.app.suid)
    table.add_row("Status", status_map[res.app.status])


    start_time = res.app.created_at.ToDatetime(tzinfo=timezone.utc).astimezone()
    end_time = res.app.updated_at.ToDatetime(tzinfo=timezone.utc).astimezone()

    color_table = Table(
        box=None,
        expand=False,
        show_header=False,
        show_edge=False,
        pad_edge=False,
    )
    color_table.add_row(
        (f"✓ {start_time} App Created.\n") +
        (f"✓ {end_time} App Stopped.\n" if res.app.status == app_pb2.AppState.STOPPED else ''),
    )

    table.add_row("Timeline", color_table)


    from rich import box

    task_table = Table(
        show_edge=False,
        show_header=True,
        expand=False,
        row_styles=["none", "dim"],
        box=box.SIMPLE,
    )
    task_table.add_column("[green]Name", style="green", no_wrap=True)
    task_table.add_column("Unique ID")
    task_table.add_column(
        "[gray]Status :white_circle:",
        style="green",
        justify="right",
        no_wrap=True,
    )
    task_table.add_column(
        "[cyan]Start Time",
        style="cyan",
        justify="right",
        no_wrap=True,
    )
    task_table.add_column(
        "[magenta]Run Time",
        style="magenta",
        justify="right",
        no_wrap=True,
    )

    for task in res.tasks[:10]:
        start_time = task.created_at.ToDatetime(tzinfo=timezone.utc).astimezone()
        end_time = task.updated_at.ToDatetime(tzinfo=timezone.utc).astimezone()
        if task.status != app_pb2.AppState.STOPPED and task.status != app_pb2.AppState.CREATED:
            end_time = datetime.now(timezone.utc)

        task_table.add_row(
            task.name,
            task.suid,
            status_map[task.status],
            start_time.strftime("%Y-%m-%d %H:%M:%S.%f %Z"),
            str(end_time - start_time)
        )

    table.add_row("Tasks", task_table)

    console.print(table)
