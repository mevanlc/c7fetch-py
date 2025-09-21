from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import rich
import typer

from c7fetch.c7 import api

from . import common, typer_util

app = typer_util.TyperAlias(module=__name__)

_QUERY_SPLIT = re.compile(r"\|")


def _normalize_queries(raw: str) -> list[str]:
    queries = [part.strip() for part in _QUERY_SPLIT.split(raw)]
    return [q for q in queries if q]


def _resolve_base_dir(output_dir: Optional[Path]) -> Path:
    if output_dir is not None:
        return (
            output_dir.expanduser() if not output_dir.is_absolute() else output_dir
        ).resolve()
    return common.config_path("search_dir")


def _should_overwrite(override: Optional[bool]) -> bool:
    if override is not None:
        return override
    return common.should_overwrite()


def _write_result(path: Path, payload: dict, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        rich.print(f"Skipping existing file: {path}")
        return
    common.write_json(path, payload)
    rich.print(f"Saved search results to {path}")


def _execute(
    query: str,
    output: Optional[Path],
    output_dir: Optional[Path],
    overwrite: Optional[bool],
) -> None:
    queries = _normalize_queries(query)
    if not queries:
        raise typer.BadParameter("At least one non-empty query is required.")

    if output and len(queries) != 1:
        raise typer.BadParameter("--output can only be used with a single query.")

    if not api.is_api_key_configured():
        rich.print(
            "Error: Context7 API key is not configured. Set one via `c7fetch config set apikey <value>` or configure `apikey_env`."
        )
        raise typer.Exit(code=1)

    base_dir = _resolve_base_dir(output_dir)
    common.ensure_directory(base_dir)
    overwrite_flag = _should_overwrite(overwrite)

    for q in queries:
        try:
            payload = api.search(q)
        except api.MissingApiKey as exc:
            rich.print(exc)
            raise typer.Exit(code=1) from None
        if output:
            target = output
        else:
            filename = common.auto_filename([q], "json")
            target = common.render_path(base_dir, filename)
        _write_result(target, payload, overwrite_flag)

    rich.print("Done.")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    query: Optional[str] = typer.Argument(
        None, help="Search query; use '|' to separate multiple queries."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Write results to this file (only valid for a single query).",
        dir_okay=False,
        writable=True,
        resolve_path=True,
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        help="Directory for generated search JSON (defaults to config search_dir).",
        file_okay=False,
        resolve_path=True,
    ),
    overwrite: Optional[bool] = typer.Option(
        None,
        "--overwrite/--no-overwrite",
        help="Override the configured overwrite behaviour for this run.",
    ),
):
    if ctx.invoked_subcommand:
        return
    if query is None:
        rich.print(ctx.command.get_help(ctx))
        raise typer.Exit(code=1)
    _execute(query, output, output_dir, overwrite)
