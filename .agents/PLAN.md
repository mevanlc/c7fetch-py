# Implementation & Fix Plan

## Current Gaps
- `c7fetch/cli/main.py` leaves `main()` unimplemented, so `python -m c7fetch.cli.main` exits silently instead of invoking the CLI.
- `c7fetch/c7/api.py` is empty; there is no reusable HTTP client for Context7, no authentication handling, and no serialization helpers.
- CLI subcommands (`search`, `fetch`, `review`) exist only as empty Typer apps, so none of the workflows described in README actually work.
- Output management (auto-naming, respecting `no_overwrite`, directory creation) is unimplemented; dependencies such as `pathvalidate` mentioned in README are also missing from `pyproject.toml`.
- Error handling and user feedback (e.g., missing API key, HTTP failures, malformed local JSON) are non-existent.

## Implementation Strategy
1. **HTTP Client Layer (`c7fetch/c7/api.py`)**
   - Implement reusable functions for `search(query: str, headers: dict)` and `fetch(library_id: str, *, tokens: int, format: str, topic: str | None)` using `requests`.
   - Read auth and client metadata from `settings` (`apikey`, `apikey_env`, `user_agent`, `request_delay`), preferring the env var if set.
   - Centralize base URL, retries/backoff, status-code handling, and JSON/text decoding; raise descriptive Typer-friendly exceptions.

2. **Utility Support**
   - Add helpers for validating/sanitizing file names (`pathvalidate` or equivalent), expanding config placeholders, and ensuring directories exist.
   - Introduce simple logger or reuse `typer.echo`/`rich` for status messaging respecting `loglevel`.
   - Update `pyproject.toml` to include `pathvalidate`, `rich` (already used implicitly), and potentially `typing-extensions` if needed.

3. **`search` CLI** (`c7fetch/cli/search.py`)
   - Implement a Typer command accepting the query (supporting multi-query input separated by `|`), optional output path override, and `--merge-into` / `--open` flags as needed.
   - Fetch results via API client, write JSON (`indent=2`) under `search_dir`, auto-name files with sanitized query, and honor `no_overwrite`.
   - Return meaningful exit codes and status messages; surface HTTP errors.

4. **`review` CLI** (`c7fetch/cli/review.py`)
   - Load one or more search result JSON files (default glob `*.json` inside `search_dir`), apply glob filtering arguments for library id/title/description.
   - Render structured tables using `rich.Table`, grouping by source file (similar to README example) with truncated descriptions for terminal width.
   - Provide `--merge` option to combine multiple files into a single table.

5. **`fetch` CLI** (`c7fetch/cli/fetch.py`)
   - Implement command to retrieve documents by `library_id_glob` and optional `title/description` glob using data from search results or direct args.
   - Respect `--format` (`text`/`json`) and `--tokens` options; default to config values.
   - Save output to `{output_dir}/{library_id}/{auto_name}.{ext}` with overwrite guard; optionally support `--topic`.

6. **Entrypoint & Packaging**
   - Update `c7fetch/cli/main.py.main()` to invoke `app()` for entrypoint parity with `python -m c7fetch.cli`. Ensure module exports `app`.
   - Add minimal smoke tests (e.g., CLI invocation with Typer's `CliRunner`) covering happy/error paths, and wire into future CI (placeholder).

## Validation Plan
- Manual CLI smoke tests against mocked API responses (use `pytest` + `responses` or `requests_mock`).
- Verify config precedence (env > file > defaults) with unit tests.
- Confirm file generation respects `no_overwrite` and directories.
- Run `ruff` for linting once implementation lands.
