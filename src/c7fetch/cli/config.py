import json
import os

import rich
import rich.table as rt
import typer

from . import settings, typer_util
from .settings import CONFIG_DIR, config_file_path

app = typer_util.TyperAlias(module=__name__)


@app.command("describe | desc")
def describe():
    """Describe available configuration settings."""
    rich.print("\n")
    table = rt.Table(title="Configuration Settings")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Default", style="green")
    for setting in settings.SCHEMA:
        table.add_row(setting.key, setting.desc, setting.default)
    rich.print(table)
    rich.print("\nUse 'c7fetch config set <key> <value>' to set a configuration.")


@app.command()
def list():
    """List all configurations."""
    rich.print("Listing all configurations...")
    config_file = config_file_path()
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
            rich.print_json(config)
    else:
        rich.print("No configuration file found.")


@app.command()
def set(key: str, value: str):
    """Set a configuration key to a value."""
    if key not in [s.key for s in settings.SCHEMA]:
        rich.print(f"Unknown configuration key: [red]{key}[/red]")
        raise typer.Exit(code=1)
    rich.print(f"Setting [green]{key}[/green] to [yellow]{value}[/yellow]")
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config = {}
    config_file = config_file_path()
    if os.path.exists(config_file):
        config = _read_config_file()
    config[key] = value
    _write_config_file(config)
    rich.print("Configuration updated.")


@app.command()
def get(key: str):
    """Get the value of a configuration key."""
    config = _read_config_file()
    if key in config:
        rich.print(f"{config[key]}")
    else:
        _config_key_not_found(key)


@app.command()
def unset(key: str):
    """Unset a configuration key."""
    config = _read_config_file()
    if key in config:
        del config[key]
        _write_config_file(config)
        rich.print(f"Configuration key [green]'{key}'[/green] unset.")
    else:
        _config_key_not_found(key)


def _write_config_file(config: dict):
    with open(config_file_path(), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def _read_config_file():
    _require_config_file()
    with open(config_file_path(), "r", encoding="utf-8") as f:
        return json.load(f)


def _config_key_not_found(key: str):
    rich.print(f"Configuration key [red]'{key}'[/red] not found.")
    raise typer.Exit(code=1)


def _require_config_file():
    config_file = config_file_path()
    if not os.path.exists(config_file):
        rich.print(f"No configuration file found at {config_file}.")
        rich.print("Please run 'c7fetch config set <key> <value>' to create one.")
        raise typer.Exit(code=1)
