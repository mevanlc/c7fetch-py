from __future__ import annotations

import fnmatch
import textwrap
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import common, typer_util

app = typer_util.TyperAlias(module=__name__)


console = Console()


def _collect_files(explicit_file: Optional[Path]) -> List[Path]:
    if explicit_file is not None:
        return [explicit_file]
    search_dir = common.config_path("search_dir")
    return sorted(search_dir.glob("*.json"))


def _matches(value: str, pattern: Optional[str]) -> bool:
    if not pattern:
        return True
    return fnmatch.fnmatch(value, pattern)


def _format_description(desc: str, width: int = 70) -> str:
    if not desc:
        return ""
    return textwrap.shorten(desc, width=width, placeholder="…")


def _rows_from_result(result: dict) -> List[str]:
    library_id = result.get("id", "-")
    title = result.get("title", "-")
    last_updated = result.get("lastUpdateDate", "-")
    stars = result.get("stars")
    trust = result.get("trustScore")
    description = result.get("description", "")

    stars_display = "-" if stars in (-1, None) else str(stars)
    trust_display = "-" if trust is None else str(trust)

    return [
        library_id,
        title,
        last_updated,
        stars_display,
        trust_display,
        _format_description(description),
    ]


def _execute(
    file: Optional[Path],
    library: Optional[str],
    title: Optional[str],
    description: Optional[str],
    merge: bool,
) -> None:
    search_files = _collect_files(file)
    if not search_files:
        typer.echo("No search result files found. Run 'c7fetch search' first.")
        raise typer.Exit(code=1)

    aggregated_rows: List[List[str]] = []

    for file_path in search_files:
        try:
            payload = common.load_json(file_path)
        except Exception as exc:  # pragma: no cover - best effort error surfacing
            typer.echo(f"Failed to read {file_path}: {exc}")
            continue
        results = payload.get("results", [])
        filtered_rows = [
            _rows_from_result(result)
            for result in results
            if _matches(result.get("id", ""), library)
            and _matches(result.get("title", ""), title)
            and _matches(result.get("description", ""), description)
        ]
        if not filtered_rows:
            typer.echo(f"No matching results in {file_path}.")
            continue

        if merge:
            aggregated_rows.extend(filtered_rows)
        else:
            table = Table(title=f"Results from: {file_path}")
            table.add_column("Library ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Last Updated", style="green")
            table.add_column("Stars", justify="right")
            table.add_column("Trust", justify="right")
            table.add_column("Description", style="dim")
            for row in filtered_rows:
                table.add_row(*row)
            console.print(table)

    if merge and aggregated_rows:
        table = Table(title="Search Results")
        table.add_column("Library ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Last Updated", style="green")
        table.add_column("Stars", justify="right")
        table.add_column("Trust", justify="right")
        table.add_column("Description", style="dim")
        for row in aggregated_rows:
            table.add_row(*row)
        console.print(table)

    typer.echo("Done.")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Specific search result JSON file to review.",
        path_type=Path,
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
    ),
    library: Optional[str] = typer.Option(
        None,
        "--library",
        "-l",
        help="Glob pattern to filter by library id.",
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        help="Glob pattern to filter by title.",
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="Glob pattern applied to description text.",
    ),
    merge: bool = typer.Option(
        False,
        "--merge",
        help="Combine all rows into a single table instead of grouping per file.",
    ),
):
    if ctx.invoked_subcommand:
        return
    _execute(file, library, title, description, merge)
