from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import rich
import typer

from c7fetch.c7 import api

from . import common, typer_util

app = typer_util.TyperAlias(module=__name__)


def _resolve_base_dir(output_dir: Optional[Path]) -> Path:
    if output_dir is not None:
        return output_dir
    return common.config_path("output_dir")


def _should_overwrite(override: Optional[bool]) -> bool:
    if override is not None:
        return override
    return common.should_overwrite()


def _extension(fmt: str) -> str:
    return "md" if fmt == "text" else "json"


def _write_payload(path: Path, payload: api.FetchResponse, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        rich.print(f"Skipping existing file: {path}")
        return
    common.ensure_directory(path.parent)
    if payload.content_type == "application/json":
        common.write_json(path, payload.payload)
    else:
        path.write_text(str(payload.payload), encoding="utf-8")
    rich.print(f"Saved fetched content to {path}")


def _execute(
    library_ids: List[str],
    tokens: Optional[int],
    fmt: str,
    topic: Optional[str],
    output: Optional[Path],
    output_dir: Optional[Path],
    overwrite: Optional[bool],
) -> None:
    if not library_ids:
        raise typer.BadParameter("Provide at least one library id to fetch.")

    if output is not None and len(library_ids) != 1:
        raise typer.BadParameter("--output is only valid when fetching a single library id.")

    fmt_normalized = fmt.lower()
    if fmt_normalized not in {"text", "json"}:
        raise typer.BadParameter("--format must be either 'text' or 'json'.")

    if not api.is_api_key_configured():
        rich.print(
            "Error: Context7 API key is not configured. Set one via `c7fetch config set apikey <value>` or configure `apikey_env`.",
        )
        raise typer.Exit(code=1)

    token_limit = tokens if tokens is not None else common.default_token_count()
    base_dir = _resolve_base_dir(output_dir)
    overwrite_flag = _should_overwrite(overwrite)

    for library_id in library_ids:
        try:
            response = api.fetch(
                library_id,
                tokens=token_limit,
                format=fmt_normalized,
                topic=topic,
            )
        except api.MissingApiKey as exc:
            rich.print(str(exc))
            raise typer.Exit(code=1) from None
        if output is not None:
            target = output
        else:
            filename = common.auto_filename([library_id, topic], _extension(fmt_normalized))
            target = common.render_path(base_dir, filename)
        _write_payload(target, response, overwrite_flag)

    rich.print("Done.")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    library_ids: List[str] = typer.Argument(
        ...,
        metavar="LIBRARY_ID",
        help="One or more library identifiers to fetch.",
    ),
    tokens: Optional[int] = typer.Option(
        None,
        "--tokens",
        "-t",
        help="Maximum tokens to request (defaults to configured token_count).",
    ),
    fmt: str = typer.Option(
        "text",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format: text or json.",
    ),
    topic: Optional[str] = typer.Option(
        None,
        "--topic",
        help="Optional topic within the library to target.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the response to this file (only with a single library id).",
        dir_okay=False,
        writable=True,
        resolve_path=True,
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        help="Directory for fetched documents (defaults to configured output_dir).",
        file_okay=False,
        resolve_path=True,
    ),
    overwrite: Optional[bool] = typer.Option(
        None,
        "--overwrite/--no-overwrite",
        help="Override configured overwrite behaviour.",
    ),
):
    if ctx.invoked_subcommand:
        return
    _execute(library_ids, tokens, fmt, topic, output, output_dir, overwrite)
