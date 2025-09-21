# TODO Phase 1: Core CLI Foundation

## Completed
- [x] Update config defaults to use `~/.config/c7fetch-dev` and scaffold required dependencies.
- [x] Implement Context7 API helper functions with auth, request delay, and error mapping.
- [x] Wire CLI entrypoint to invoke the Typer application.
- [x] Build `search`, `fetch`, and `review` commands with file management and config integration.
- [x] Add shared CLI utilities for path handling and sanitisation.
- [x] Extend `pyproject.toml` with runtime (`rich`, `pathvalidate`) and dev (`pytest`, `responses`) dependencies.
- [x] Introduce CLI-focused unit tests using `CliRunner` and API stubs.
- [x] Run `ruff` to validate style and imports.

## Follow-ups
- [ ] Add structured logging / verbosity controls keyed off `loglevel`.
- [ ] Expand `fetch` to support batch selection from cached search results and library globbing.
- [ ] Surface result counts and summaries in `search`/`review` output for quicker triage.
- [ ] Add retry/backoff strategy for transient API failures (5xx/429).
- [ ] Document new command options and examples in `README.md`.
- [ ] Enable automated test execution (ensure `pytest` installed in local env or CI).
