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


latest_version = "9.8.7"

def fixture_download(url):
    for repo, plugin, version in [
        ("polyipseity/obsidian-terminal", "terminal", latest_version),
        ("Vinzent03/obsidian-git", "obsidian-git", latest_version),
        ("owjxyz/Obsidian-Superier-Highlighter", "superier-highlighter", latest_version),
    ]:
        if url == f"https://api.github.com/repos/{repo}/releases/latest":
            return json.dumps({"tag_name": "v" + version, "assets": [
                {"name": name} for name in ["manifest.json", "main.js", "styles.css"]
            ]}).encode()
        prefix = f"https://github.com/{repo}/releases/download/v{version}/"
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
        "other-plugin", "terminal", "obsidian-git", "superier-highlighter"
    ]
    assert json.loads((config / "plugins/terminal/data.json").read_text())["defaultProfile"] == "darwinIntegratedDefault"
    git_settings = json.loads((config / "plugins/obsidian-git/data.json").read_text())
    assert (git_settings["autoSaveInterval"], git_settings["autoPushInterval"], git_settings["autoPullInterval"]) == (10, 60, 60)
    keys = json.loads((config / "hotkeys.json").read_text())
    assert keys["app:open-settings"] == [{"modifiers": ["Mod"], "key": ","}]
    for color, key in [("red", "A"), ("orange", "D"), ("yellow", "S"), ("green", "Z"), ("blue", "C"), ("purple", "X")]:
        assert keys[f"editor:toggle-highlight-{color}"] == [{"modifiers": ["Alt"], "key": key}]
    for color, key in [(1, "A"), (2, "D"), (3, "S"), (4, "Z"), (5, "C"), (6, "X")]:
        assert keys[f"superier-highlighter:apply-color-{color}"] == [{"modifiers": ["Ctrl"], "key": key}]
    assert keys["terminal:find-in-terminal"] == [{"modifiers": ["Alt"], "key": "F"}]
    assert keys["terminal:close-terminal"] == [{"modifiers": ["Alt"], "key": "W"}]
    assert keys["terminal:open-terminal.integrated.root"] == [
        {"key": "H", "modifiers": ["Mod", "Shift"]},
        {"modifiers": ["Alt"], "key": "T"},
    ]
    assert json.loads((config / "plugins/superier-highlighter/data.json").read_text()) == {}
    assert (vault / "note.md").read_text() == "Do not touch this note."
    before = snapshot(vault)
    assert setup.install(vault) is None
    assert snapshot(vault) == before

    latest_version = "9.8.8"
    setup.install(vault)
    assert json.loads((config / "plugins/terminal/manifest.json").read_text())["version"] == latest_version
    assert json.loads((config / "plugins/superier-highlighter/manifest.json").read_text())["version"] == latest_version

    for only, wanted, unwanted in [("terminal", "terminal", "obsidian-git"), ("git", "obsidian-git", "terminal"),
                                  ("highlighter", "superier-highlighter", "terminal")]:
        single = root / only
        (single / ".obsidian").mkdir(parents=True)
        setup.install(single, only=only)
        assert (single / ".obsidian/plugins" / wanted / "main.js").is_file()
        assert not (single / ".obsidian/plugins" / unwanted).exists()
        if only == "git":
            assert not (single / ".obsidian/hotkeys.json").exists()
        else:
            scoped = json.loads((single / ".obsidian/hotkeys.json").read_text())
            assert all(command.startswith((wanted + ":", "editor:toggle-highlight")) for command in scoped)
            assert len(scoped) == (3 if only == "terminal" else 14)

    shortcuts = root / "shortcuts"
    (shortcuts / ".obsidian").mkdir(parents=True)
    def no_download(url):
        raise AssertionError("Shortcut-only setup must not download plugins")
    setup.download = no_download
    setup.install(shortcuts, only="shortcuts")
    assert not (shortcuts / ".obsidian/plugins").exists()
    assert not (shortcuts / ".obsidian/community-plugins.json").exists()
    saved = json.loads((shortcuts / ".obsidian/hotkeys.json").read_text())
    assert saved["superier-highlighter:apply-color-5"] == [{"modifiers": ["Ctrl"], "key": "C"}]
    assert saved["superier-highlighter:apply-color-2"] == [{"modifiers": ["Ctrl"], "key": "D"}]
    assert saved["superier-highlighter:remove-highlight"] == [{"modifiers": ["Ctrl"], "key": "Q"}]
    assert saved["editor:toggle-highlight"] == [{"modifiers": ["Alt"], "key": "Q"}]
    setup.download = fixture_download

    # Retiring the old plugin also retires its shortcut bindings, preserving other settings.
    migration = root / "migration"
    migration_config = migration / ".obsidian"
    migration_config.mkdir(parents=True)
    (migration_config / "community-plugins.json").write_text('["other", "reader-highlighter-tags"]')
    (migration_config / "hotkeys.json").write_text(json.dumps({
        "reader-highlighter-tags:apply-color-1": [{"modifiers": ["Ctrl"], "key": "A"}],
        "other:command": [{"modifiers": ["Shift"], "key": "Y"}]
    }))
    setup.install(migration, only="reader")
    assert json.loads((migration_config / "community-plugins.json").read_text()) == ["other", "superier-highlighter"]
    migrated = json.loads((migration_config / "hotkeys.json").read_text())
    assert not any(command.startswith("reader-highlighter-tags:") for command in migrated)
    assert "other:command" in migrated

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
    (failing_config / "hotkeys.json").write_text('{"other":[{"modifiers":["Alt"],"key":"A"}]}')
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

    # Collision checks must cover Terminal and Reader modifiers, not just Alt+colors.
    for only, modifier, key in [("terminal", "Alt", "W"), ("highlighter", "Ctrl", "Q")]:
        (failing_config / "hotkeys.json").write_text(json.dumps({
            "unrelated": [{"modifiers": [modifier], "key": key}, {"modifiers": ["Shift"], "key": "X"}]
        }))
        before = snapshot(failing)
        try:
            setup.install(failing, only=only)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{only} shortcut conflict was accepted.")
        assert snapshot(failing) == before
        setup.install(failing, only=only, replace_conflicts=True)
        assert json.loads((failing_config / "hotkeys.json").read_text())["unrelated"] == [
            {"modifiers": ["Shift"], "key": "X"}
        ]

    # Latest-release metadata, manifests and asset digests must fail before writes.
    for problem in ["preview", "missing", "manifest", "digest"]:
        def invalid_download(url):
            content = fixture_download(url)
            if url.endswith("/releases/latest"):
                release = json.loads(content)
                if problem == "preview":
                    release["prerelease"] = True
                elif problem == "missing":
                    release["assets"] = []
                elif problem == "digest":
                    release["assets"][0]["digest"] = "sha256:" + "0" * 64
                return json.dumps(release).encode()
            if problem == "manifest" and url.endswith("manifest.json"):
                return b'{"id":"wrong","version":"9.8.8"}'
            return content
        setup.download = invalid_download
        before = snapshot(failing)
        try:
            setup.install(failing, only="git")
            raise AssertionError(f"Accepted invalid release: {problem}")
        except ValueError:
            pass
        assert snapshot(failing) == before

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
