import json

import pytest
from typer.testing import CliRunner

from c7fetch.c7 import api
from c7fetch.cli import common, fetch, review, search, settings


@pytest.fixture()
def config_setup(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "config.json"
    config = {
        "output_dir": str(tmp_path / "out"),
        "apikey": "test-key",
        "token_count": "1234",
    }
    config_file.write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.setattr(settings, "CONFIG_DIR", str(config_dir))
    monkeypatch.setattr(settings, "CONFIG_FILE", str(config_file))
    yield


def test_search_command_writes_results(tmp_path, monkeypatch, config_setup):
    runner = CliRunner()
    monkeypatch.setattr(api, "search", lambda query: {"query": query, "results": []})

    result = runner.invoke(search.app, ["React Docs"])

    assert result.exit_code == 0, result.stdout
    search_dir = common.config_path("search_dir")
    expected_file = search_dir / common.auto_filename(["React Docs"], "json")
    assert expected_file.exists()
    data = json.loads(expected_file.read_text(encoding="utf-8"))
    assert data["query"] == "React Docs"
    assert "Saved search results" in result.stdout


def test_fetch_command_writes_file(tmp_path, monkeypatch, config_setup):
    runner = CliRunner()

    def fake_fetch(library_id, **kwargs):
        return api.FetchResponse(payload="# Sample", content_type="text/markdown")

    monkeypatch.setattr(api, "fetch", fake_fetch)

    result = runner.invoke(fetch.app, ["/libs/react"])

    assert result.exit_code == 0, result.stdout
    output_dir = common.config_path("output_dir")
    expected_file = output_dir / common.auto_filename(["/libs/react", None], "md")
    assert expected_file.exists()
    assert expected_file.read_text(encoding="utf-8") == "# Sample"
    assert "Saved fetched content" in result.stdout


def test_search_requires_api_key(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(api, "is_api_key_configured", lambda: False)

    def fail_search(_query):  # pragma: no cover - safety guard
        raise AssertionError("search should not be invoked when API key is missing")

    monkeypatch.setattr(api, "search", fail_search)

    result = runner.invoke(search.app, ["React Docs"])

    assert result.exit_code == 1
    assert "API key is not configured" in result.stderr


def test_fetch_requires_api_key(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(api, "is_api_key_configured", lambda: False)

    def fail_fetch(*_args, **_kwargs):  # pragma: no cover - safety guard
        raise AssertionError("fetch should not be invoked when API key is missing")

    monkeypatch.setattr(api, "fetch", fail_fetch)

    result = runner.invoke(fetch.app, ["/libs/react"])

    assert result.exit_code == 1
    assert "API key is not configured" in result.stderr


def test_review_command_renders_table(tmp_path, config_setup):
    runner = CliRunner()
    search_dir = common.config_path("search_dir")
    common.ensure_directory(search_dir)
    payload = {
        "results": [
            {
                "id": "/libs/react",
                "title": "React",
                "description": "React description",
                "lastUpdateDate": "2025-09-05T18:55:17.104Z",
                "stars": 42,
                "trustScore": 9.1,
            }
        ]
    }
    search_file = search_dir / "react.json"
    common.write_json(search_file, payload)

    result = runner.invoke(review.app, ["--merge"])

    assert result.exit_code == 0, result.stdout
    assert "React" in result.stdout
    assert "Done." in result.stdout


def test_resolve_api_key_prefers_env(monkeypatch):
    monkeypatch.setattr(
        api.settings,
        "get_setting",
        lambda key: {"apikey_env": "C7_KEY", "apikey": "file-key"}.get(key, ""),
    )
    monkeypatch.setenv("C7_KEY", "env-value")
    assert api._resolve_api_key() == "env-value"
