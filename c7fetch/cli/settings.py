import functools
import json
import os
import re
from dataclasses import dataclass

CONFIG_DIR = os.path.expanduser("~/.config/c7fetch-dev")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


@dataclass
class SettingDesc:
    key: str
    desc: str
    default: str = ""


S_APIKEY = SettingDesc(key="apikey", desc="Context7 API key")
S_APIKEY_ENV = SettingDesc(
    key="apikey_env", desc="Context7 API key (read from env var)"
)
S_OUTPUT_DIR = SettingDesc(
    key="output_dir", desc="Directory to save fetched files", default="./c7docs"
)
S_SEARCH_DIR = SettingDesc(
    key="search_dir",
    desc="Directory to save search results",
    default="{output_dir}/search",
)
S_LOGLEVEL = SettingDesc(key="loglevel", desc="Logging level", default="INFO")
S_TOKEN_COUNT = SettingDesc(
    key="token_count", desc="Default token count for requests", default="10000"
)
S_NO_OVERWRITE = SettingDesc(
    key="no_overwrite", desc="Do not overwrite existing files", default="false"
)
S_DEFAULT_FORMAT = SettingDesc(
    key="default_format",
    desc="Default format for fetched documents (text or json)",
    default="text",
)
S_USER_AGENT = SettingDesc(
    key="user_agent",
    desc="User-Agent string to use in API requests",
    default="c7fetch/{c7fetch_version}",
)
S_REQUEST_DELAY = SettingDesc(
    key="request_delay",
    desc="Delay between API requests (in milliseconds)",
    default="1000",
)

SCHEMA = [
    S_APIKEY,
    S_APIKEY_ENV,
    S_OUTPUT_DIR,
    S_SEARCH_DIR,
    S_LOGLEVEL,
    S_TOKEN_COUNT,
    S_NO_OVERWRITE,
    S_DEFAULT_FORMAT,
    S_USER_AGENT,
    S_REQUEST_DELAY,
]

SETTINGS_KEY2DESC = {s.key: s for s in SCHEMA}
SETTINGS_KEY2DEFAULT = {s.key: s.default for s in SCHEMA}


def get_setting_with_default(key: str) -> str:
    """Get a configuration setting or its default value."""
    if not os.path.exists(CONFIG_FILE):
        return SETTINGS_KEY2DEFAULT.get(key, "")
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    return config.get(key, SETTINGS_KEY2DEFAULT.get(key, ""))


@functools.lru_cache(maxsize=None)
def _get_version() -> str:
    try:
        import importlib.metadata

        return importlib.metadata.version("c7fetch")
    except Exception:
        return "0.0.0"


def _get_replacement_value(key: str) -> str:
    if key == "c7fetch_version":
        return _get_version()
    if key not in SETTINGS_KEY2DESC:
        raise ValueError(f"Unknown setting placeholder: {key}")
    return get_setting_with_default(key)


RE_PLACEHOLDER = re.compile(r"\{([^}]+)\}")


def get_setting(key: str) -> str:
    """Get a configuration setting and apply replacements."""
    value = get_setting_with_default(key)

    def replace_match(m):
        return _get_replacement_value(m.group(1))

    return RE_PLACEHOLDER.sub(replace_match, value)
