# Architectural & Security Notes

- **API key storage**: Current config workflow persists secrets in `~/.config/c7fetch/config.json` without encryption. Prefer reading from `apikey_env` or prompting users, and document risks of storing plaintext keys.
- **Auth header handling**: Ensure the forthcoming HTTP client never logs the raw `Authorization` header and strips it from exception messages.
- **Output path sanitization**: When auto-naming files based on user input, sanitize aggressively to prevent directory traversal or invalid filenames before touching the filesystem.
- **Rate limiting / polite usage**: Respect `request_delay` between fetches to avoid hammering Context7. Consider exponential backoff on 429/5xx responses.
- **Error propagation**: Wrap network/JSON errors so the CLI exits cleanly with actionable messaging instead of tracebacks; this keeps the UX predictable for scripting.
- **Dependency surface**: Adding `rich` and `pathvalidate` increases attack surface; pin versions and document supply-chain expectations. Use virtual environment isolation by default.
