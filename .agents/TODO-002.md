# TODO Phase 2: Polishing & Resilience

## Logging & Observability
- [ ] Honour `loglevel` setting across commands with structured Typer/Rich logging helpers.
- [ ] Add verbose mode (`--verbose`) to surface request URLs, payload sizes, and rate-limit waits when troubleshooting.
- [ ] Ensure API errors redact credentials and include actionable remediation hints.

## Fetch & Review Enhancements
- [ ] Allow `fetch` to accept glob patterns or multiple IDs resolved via cached search files.
- [ ] Surface summary metadata (result counts, most recent update) after `search` completes.
- [ ] Add optional CSV/table export for `review` when `--merge` is active.
- [ ] Implement duplicate detection when aggregating results across multiple search files.

## Reliability & Error Handling
- [ ] Introduce retry/backoff (e.g., exponential with jitter) for transient 429/5xx responses.
- [ ] Time out long-running requests based on configurable threshold; surface elapsed time in errors.
- [ ] Validate saved JSON/text files immediately after write to catch partial writes.

## Documentation & DX
- [ ] Update README with CLI examples covering new flags plus configuration guidance.
- [ ] Provide sample config (`.c7fetch/config.sample.json`) showcasing env-var usage.
- [ ] Add developer quickstart docs (install extras, run tests, lint) in README or CONTRIBUTING.

## Testing & QA
- [ ] Ensure `pytest` runs locally by baking dev extra into `requirements-dev.txt` or documentation.
- [ ] Expand tests to cover `review --merge` and error paths (missing files, invalid JSON).
- [ ] Mock retry/backoff paths to guarantee deterministic behaviour under failure states.

## Security & Packaging
- [ ] Mask API key values in logs/config list output; include security note in docs.
- [ ] Evaluate packaging for distribution (set classifiers, description) before publishing to PyPI.
- [ ] Consider adding `pre-commit` hook config for `ruff` and formatting checks.
