# c7fetch Implementation & Fix Plan

## Current Snapshot (2025-09-21)
- CLI surface (config/search/fetch/review) is implemented with shared utilities and tests for the happy paths.
- Context7 API client supports search/fetch with rate limiting and error types but relies on callers to surface errors.
- Bug: `search` and `fetch` commands allow `MissingApiKey` to bubble, leading to a raw stack trace when credentials are absent or misconfigured.

## Immediate Objectives
1. **CLI API-key Preflight & Messaging**
   - Add a lightweight helper in `c7fetch.c7.api` to detect whether credentials are present.
   - Update `search` and `fetch` command execution paths to fail fast with a clear, user-facing error when no key is configured.
   - Catch `MissingApiKey` raised mid-flight (e.g., stale env var) and exit cleanly instead of propagating.
   - Extend CLI tests to cover the missing-key scenarios for both commands.

2. **Error Surface Consistency** *(next after Objective 1)*
   - Audit other `ApiError` paths (e.g., HTTP 429/500) and ensure the CLI translates them into helpful messages and non-zero exit codes.
   - Consider a shared error handler module to keep Typer callbacks concise.

## Near-Term Enhancements & Tech Debt
- Mask sensitive values (API keys) in `config list` output and consider warnings when persisting credentials to disk.
- Add richer UX cues (result summaries for `search`, progress indicators for multi-fetch) once core error handling is solidified.
- Expand review command coverage: regression tests for `--merge`, empty datasets, and malformed JSON handling.
- Document credential setup best practices (env vars, config file location) in `README.md` alongside troubleshooting notes.

## Testing & Validation Strategy
- Continue using `CliRunner` with monkeypatched API calls for deterministic CLI tests.
- Add targeted unit tests around any new helper functions (e.g., credential detection) if behavior becomes more complex.
- Run `pytest` and `ruff` before shipping changes; add CI hooks as follow-up work.
