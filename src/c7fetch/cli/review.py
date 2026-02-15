import fnmatch
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import typing

import rich
import typer
from rich.console import Console
from rich.table import Table, Column

from c7fetch.table import NegColTable

from . import common, typer_util

app = typer_util.TyperAlias(module=__name__)


console = Console()

term_width = console.size.width


def _collect_files(explicit_file: Optional[Path]) -> List[Path]:
    if explicit_file is not None:
        return [explicit_file]
    search_dir = common.config_path("search_dir")
    return sorted(search_dir.glob("*.json"))


def _matches(value: str, pattern: Optional[str]) -> bool:
    if not pattern:
        return True
    return fnmatch.fnmatch(value, pattern)


def _current_time() -> datetime:
    """Return the current UTC time.

    Separated into a helper so tests can monkeypatch a stable value.
    """

    return datetime.now(timezone.utc)


def _humanize_last_updated(raw_value: typing.Optional[str]) -> str:
    if not raw_value:
        return "-"
    if raw_value == "-":
        return raw_value

    normalized = raw_value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return raw_value

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    delta = _current_time() - parsed
    total_seconds = delta.total_seconds()
    if total_seconds <= 0:
        days = 0
    else:
        days = math.ceil(total_seconds / 86400)
    unit = "day" if days == 1 else "days"
    return f"{days} {unit}"


def _rows_from_result(result: dict[str, str]) -> List[str]:
    library_id = result.get("id", "-")
    title = result.get("title", "-")
    last_updated = _humanize_last_updated(result.get("lastUpdateDate"))
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
        description,
    ]


def _configure_table(table: Table, rows: List[list[str]]) -> None:
    def col_idx_gen():
        for idx in range(len(rows[0])):
            yield idx

    col_indices = col_idx_gen()
    columns = [
        Column(_index=next(col_indices), header="ID", style="cyan", no_wrap=True),
        Column(_index=next(col_indices), header="Title", style="magenta", no_wrap=True),
        Column(_index=next(col_indices), header="Updated", style="green", no_wrap=True),
        Column(_index=next(col_indices), header="⭐", no_wrap=True),
        Column(_index=next(col_indices), header="Trust", no_wrap=True),
        Column(_index=next(col_indices), header="Description", 
               style="dim", 
               no_wrap=True, 
               width=-1),
    ]

    # debug_display_col_cfg(columns)

    for column in columns:
        table.columns.append(column)


# def debug_display_col_cfg(colconfigs: List[Column]) -> None:
#     tab = Table(title="Column Config Debug")
#     kwarg_names = [k for k in colconfigs[0].rich_col_kwargs.keys()]
#     for kwarg_name in kwarg_names:
#         tab.add_column(kwarg_name)
#     for colconfig in colconfigs:
#         row = [str(colconfig.rich_col_kwargs.get(k, "")) for k in kwarg_names]
#         tab.add_row(*row)
#     console.print(tab)


def _execute(
    file: Optional[Path],
    library: Optional[str],
    title: Optional[str],
    description: Optional[str],
    merge: bool,
) -> None:
    search_files = _collect_files(file)
    if not search_files:
        rich.print("No search result files found. Run 'c7fetch search' first.")
        raise typer.Exit(code=1)

    aggregated_rows: List[List[str]] = []

    for file_path in search_files:
        try:
            payload = common.load_json(file_path)
        except Exception as exc:  # pragma: no cover - best effort error surfacing
            rich.print(f"Failed to read {file_path}: {exc}")
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
            rich.print(f"No matching results in {file_path}.")
            continue

        if merge:
            aggregated_rows.extend(filtered_rows)
        else:
            table = _new_table(f"Results from: {file_path}", filtered_rows)
            for row in filtered_rows:
                table.add_row(*row)
            console.print(table)

    if merge and aggregated_rows:
        table = _new_table("Search Results", aggregated_rows)
        for row in aggregated_rows:
            table.add_row(*row)
        console.print(table)

    rich.print("Done.")

def _new_table(title:str, aggregated_rows: List[List[str]]) -> NegColTable:
    table = NegColTable(title=title)
    _configure_table(table, aggregated_rows)
    return table


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Specific search result JSON file to review.",
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
