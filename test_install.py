"""Run with python3 test_install.py. All writes use temporary vaults."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT = Path(__file__).with_name("install.py")
assert SCRIPT.is_file(), "The standalone installer must exist."
spec = importlib.util.spec_from_file_location("vault_setup", SCRIPT)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def fixture_download(url):
    for repo, plugin, version in [
        ("polyipseity/obsidian-terminal", "terminal", "3.29.0"),
        ("Vinzent03/obsidian-git", "obsidian-git", "2.42.0"),
    ]:
        prefix = f"https://github.com/{repo}/releases/download/{version}/"
        if url.startswith(prefix):
            name = url[len(prefix):]
            if name == "manifest.json":
                return json.dumps({"id": plugin, "version": version}).encode()
            if name in {"main.js", "styles.css"}:
                return f"fixture {plugin} {name}".encode()
    raise AssertionError(f"Unexpected download: {url}")


def snapshot(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


setup.download = fixture_download
with TemporaryDirectory() as folder:
    root = Path(folder)
    vault = root / "테스트 Vault"
    config = vault / ".obsidian"
    config.mkdir(parents=True)
    (vault / "note.md").write_text("Do not touch this note.")
    (config / "community-plugins.json").write_text('["other-plugin"]')
    original = b'{"app:open-settings":[{"modifiers":["Mod"],"key":","}]}\n'
    (config / "hotkeys.json").write_bytes(original)
    backup = setup.install(vault)
    assert backup and (backup / "hotkeys.json").read_bytes() == original
    assert json.loads((config / "community-plugins.json").read_text()) == [
        "other-plugin", "terminal", "obsidian-git"
    ]
    assert json.loads((config / "plugins/terminal/data.json").read_text())["defaultProfile"] == "darwinIntegratedDefault"
    git_settings = json.loads((config / "plugins/obsidian-git/data.json").read_text())
    assert (git_settings["autoSaveInterval"], git_settings["autoPushInterval"], git_settings["autoPullInterval"]) == (10, 60, 60)
    keys = json.loads((config / "hotkeys.json").read_text())
    assert keys["app:open-settings"] == [{"modifiers": ["Mod"], "key": ","}]
    for color, key in [("red", "1"), ("orange", "2"), ("yellow", "Q"), ("green", "A"), ("blue", "S"), ("purple", "Z")]:
        assert keys[f"editor:toggle-highlight-{color}"] == [{"modifiers": ["Alt"], "key": key}]
    assert (vault / "note.md").read_text() == "Do not touch this note."
    before = snapshot(vault)
    assert setup.install(vault) is None
    assert snapshot(vault) == before

    for only, wanted, unwanted in [("terminal", "terminal", "obsidian-git"), ("git", "obsidian-git", "terminal")]:
        single = root / only
        (single / ".obsidian").mkdir(parents=True)
        setup.install(single, only=only)
        assert (single / ".obsidian/plugins" / wanted / "main.js").is_file()
        assert not (single / ".obsidian/plugins" / unwanted).exists()
        assert not (single / ".obsidian/hotkeys.json").exists()

    # Bad settings, conflicts and download errors must not make partial installs.
    failing = root / "failing"
    failing_config = failing / ".obsidian"
    failing_config.mkdir(parents=True)
    for contents in ["{", "{}"]:
        (failing_config / "community-plugins.json").write_text(contents)
        before = snapshot(failing)
        try:
            setup.install(failing)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid community plugin list was accepted.")
        assert snapshot(failing) == before
    (failing_config / "community-plugins.json").write_text("[]")
    (failing_config / "hotkeys.json").write_text('{"other":[{"modifiers":["Alt"],"key":"1"}]}')
    before = snapshot(failing)
    try:
        setup.install(failing)
    except ValueError:
        pass
    else:
        raise AssertionError("Conflicting shortcuts were accepted.")
    assert snapshot(failing) == before
    setup.install(failing, replace_conflicts=True)
    assert json.loads((failing_config / "hotkeys.json").read_text())["other"] == []

    def failed_download(url):
        raise OSError("Simulated download failure")

    setup.download = failed_download
    before = snapshot(failing)
    try:
        setup.install(failing, only="terminal")
    except OSError:
        pass
    else:
        raise AssertionError("Download failure was ignored.")
    assert snapshot(failing) == before

    # If a write fails halfway through, restore already replaced files.
    setup.download = fixture_download
    real_write = setup.atomic_write
    attempts = []

    def fail_second_write(path, content):
        attempts.append(path)
        if len(attempts) == 2:
            raise OSError("Simulated write failure")
        return real_write(path, content)

    (config / "plugins/terminal/main.js").write_bytes(b"old terminal code")
    (config / "plugins/terminal/styles.css").write_bytes(b"old terminal css")
    setup.atomic_write = fail_second_write
    try:
        setup.install(vault, only="terminal")
    except OSError:
        pass
    else:
        raise AssertionError("Write failure was ignored.")
    assert (config / "plugins/terminal/main.js").read_bytes() == b"old terminal code"
    assert (config / "plugins/terminal/styles.css").read_bytes() == b"old terminal css"
    setup.atomic_write = real_write

    try:
        setup.install(root)
    except ValueError:
        pass
    else:
        raise AssertionError("A non-vault was accepted.")
    assert not (root / ".obsidian").exists()

print("PASS: all, per-plugin installs, settings, preservation, backups, repeat apply, conflicts, failures, rollback")
