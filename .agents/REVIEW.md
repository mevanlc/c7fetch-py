# Architectural & Security Notes (2025-09-21)

## Credential Handling
- `config list` currently dumps the configuration JSON verbatim, including the API key. We should redact or mask credential values before printing to avoid leaking secrets to terminal history or logs.
- API keys are stored in plain text under `~/.config/c7fetch-dev/config.json`. Encourage the `apikey_env` workflow in docs and consider warning the user (or asking for confirmation) before persisting secrets to disk.
- Nothing prevents someone from configuring `apikey_env` to an unset variable; combined with the lack of early checks this yields confusing runtime failures. The planned preflight will mitigate the UX, but longer term we could validate the env var presence when the setting is saved.

## Error Propagation
- Typer callbacks largely defer to the API layer. When any `ApiError` other than simple validation occurs, the user sees a traceback. We should centralize error mapping (e.g., decorator or shared helper) so that `HttpError` and network failures produce friendly messages with actionable hints.
- Consider emitting exit codes that downstream scripts can parse (e.g., distinct codes for auth vs transient HTTP failures) if we expect automation usage.

## Path & File Safety
- Relative config paths are resolved against the *current working directory* via `Path.cwd()`. Running the CLI from different directories could scatter output unexpectedly. We may want to resolve the base once (e.g., when saving the config) or document the behavior clearly.
- Overwrite protection is opt-out, but we currently overwrite without prompting even when `typer.Option` `--output` targets an existing file. We should warn users unless `--overwrite` is provided explicitly.

## Observability & Testing
- The project lacks logging; troubleshooting relies on ad-hoc prints. We should funnel through `rich`/`logging` keyed off the existing `loglevel` setting.
- Test coverage does not exercise `review --merge`, error branches, or simulated HTTP failures. Adding mocks for `HttpError`/`MissingApiKey` in CLI tests will help prevent regressions.
