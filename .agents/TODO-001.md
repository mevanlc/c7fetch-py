# TODO Phase 1 – Error Handling Hardening

## In Progress
- [x] Add a credential preflight helper in `c7fetch.c7.api` to let commands detect missing API keys without making a request.
- [x] Update `search` and `fetch` command implementations to use the helper, print a friendly error, and exit with status 1 when credentials are absent.
- [x] Extend CLI tests to cover the missing-key path for both commands.

## Up Next
- [ ] Introduce shared CLI error handling so other `ApiError` subclasses surface as readable messages instead of tracebacks.
- [ ] Document preferred credential setup (env var vs config file) in the README once UX is improved.
