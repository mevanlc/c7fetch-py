# Phase 1 TODOs

- [ ] Implement Context7 API client in `c7fetch/c7/api.py` with auth + error handling.
- [ ] Wire `c7fetch/cli/main.py.main()` to invoke the Typer app entrypoint.
- [ ] Flesh out `search` command (multi-query input, JSON output, auto-naming, config awareness).
- [ ] Flesh out `fetch` command (format selection, token defaults, file-writing with `no_overwrite`).
- [ ] Implement `review` command to render Rich tables from stored search JSON.
- [ ] Add missing dependencies (`rich`, `pathvalidate`, tooling for tests) to `pyproject.toml`.
- [ ] Introduce unit tests for CLI flows and config precedence.
- [ ] Run `ruff` and address lint/style issues introduced during implementation.
