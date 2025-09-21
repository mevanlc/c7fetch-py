import json
import os
from dataclasses import dataclass

import rich
import typer

from . import typer_util

app = typer_util.TyperAlias(module=__name__)

CONFIG_DIR = os.path.expanduser("~/.config/c7fetch")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

@dataclass
class SettingDesc:
    key: str
    desc: str
    default: str = ""


SETTINGS = [
    SettingDesc(key="apikey", desc="Context7 API key"),
    SettingDesc(key="apikey_env", desc="Context7 API key (read from env var)"),
    SettingDesc(key="output_dir", desc="Directory to save fetched files", default="./c7docs"),
    SettingDesc(key="search_dir", desc="Directory to save search results", default="{output_dir}/search"),
    SettingDesc(key="loglevel", desc="Logging level", default="INFO"),
]

@app.command("describe | desc")
def describe():
    """Describe available configuration settings."""
    typer.echo("\n")
    import rich.table as rt
    table = rt.Table(title="Configuration Settings")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Default", style="green")  
    for setting in SETTINGS:
        table.add_row(setting.key, setting.desc, setting.default)
    rich.print(table)
    typer.echo("\nUse 'c7fetch config set <key> <value>' to set a configuration.")

@app.command()
def list():
    """List all configurations."""
    typer.echo("Listing all configurations...")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            rich.print_json(data=config)
    else:
        typer.echo("No configuration file found.")

@app.command()
def set(key: str, value: str):
    """Set a configuration key to a value."""
    if key not in [s.key for s in SETTINGS]:
        typer.echo(f"Unknown configuration key: {key}")
        raise typer.Exit(code=1)
    typer.echo(f"Setting {key} to {value}...")
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    config[key] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    typer.echo("Configuration updated.")


@app.command()
def get(key: str):
    """Get the value of a configuration key."""
    if not os.path.exists(CONFIG_FILE):
        typer.echo("No configuration file found.")
        raise typer.Exit(code=1)
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    if key in config:
        typer.echo(f"{config[key]}")
    else:
        typer.echo(f"Configuration key '{key}' not found.")
        raise typer.Exit(code=1)

@app.command()
def unset(key: str):
    """Unset a configuration key."""
    if not os.path.exists(CONFIG_FILE):
        typer.echo("No configuration file found.")
        raise typer.Exit(code=1)
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    if key in config:
        del config[key]
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        typer.echo(f"Configuration key '{key}' unset.")
    else:
        typer.echo(f"Configuration key '{key}' not found.")
        raise typer.Exit(code=1)
