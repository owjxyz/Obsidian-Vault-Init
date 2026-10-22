#!/usr/bin/env python3
"""Install saved plugin settings and shortcuts into an existing Obsidian vault."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.request
from urllib.parse import quote
import hashlib

# Settings snapshots from the source vault; no plugin binaries or credentials.
SETTINGS = json.loads(r'''{
  "terminal": {
    "addToCommand": true,
    "addToContextMenu": true,
    "createInstanceNearExistingOnes": true,
    "errorNoticeTimeout": 0,
    "experiments": {},
    "exposeInternalModules": true,
    "focusOnNewInstance": true,
    "hideStatusBar": "focused",
    "showTerminalTabPrefix": false,
    "tabStatus": "animated",
    "interceptKeysWhenFocused": true,
    "interceptLogging": true,
    "keymappings": [
      {
        "action": "sendEscapeSequence",
        "actionArg": "\r",
        "alt": false,
        "ctrl": false,
        "key": "Enter",
        "meta": false,
        "platform": null,
        "shift": true
      },
      {
        "action": "scrollPages",
        "actionArg": -1,
        "alt": false,
        "ctrl": false,
        "key": "PageUp",
        "meta": false,
        "platform": null,
        "shift": false
      },
      {
        "action": "scrollPages",
        "actionArg": 1,
        "alt": false,
        "ctrl": false,
        "key": "PageDown",
        "meta": false,
        "platform": null,
        "shift": false
      },
      {
        "action": "scrollToTop",
        "actionArg": null,
        "alt": false,
        "ctrl": false,
        "key": "Home",
        "meta": false,
        "platform": null,
        "shift": false
      },
      {
        "action": "scrollToBottom",
        "actionArg": null,
        "alt": false,
        "ctrl": false,
        "key": "End",
        "meta": false,
        "platform": null,
        "shift": false
      },
      {
        "action": "sendEscapeSequence",
        "actionArg": "b",
        "alt": true,
        "ctrl": false,
        "key": "ArrowLeft",
        "meta": false,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendEscapeSequence",
        "actionArg": "f",
        "alt": true,
        "ctrl": false,
        "key": "ArrowRight",
        "meta": false,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendHexCode",
        "actionArg": "01",
        "alt": false,
        "ctrl": false,
        "key": "ArrowLeft",
        "meta": true,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendHexCode",
        "actionArg": "05",
        "alt": false,
        "ctrl": false,
        "key": "ArrowRight",
        "meta": true,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendHexCode",
        "actionArg": "17",
        "alt": true,
        "ctrl": false,
        "key": "Backspace",
        "meta": false,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendHexCode",
        "actionArg": "15",
        "alt": false,
        "ctrl": false,
        "key": "Backspace",
        "meta": true,
        "platform": "darwin",
        "shift": false
      },
      {
        "action": "sendEscapeSequence",
        "actionArg": "d",
        "alt": true,
        "ctrl": false,
        "key": "Delete",
        "meta": false,
        "platform": "darwin",
        "shift": false
      }
    ],
    "language": "",
    "macOSOptionKeyPassthrough": true,
    "rightClickAction": "copyPaste",
    "newInstanceBehavior": "newRightTab",
    "noticeTimeout": 5,
    "openChangelogOnUpdate": true,
    "pinNewInstance": true,
    "preferredRenderer": "webgl",
    "prewarmConPty": true,
    "windowsTerminalConsoleHost": true,
    "pythonExecutable": "",
    "profiles": {
      "darwinExternalDefault": {
        "args": [
          "\"$PWD\""
        ],
        "environment": [],
        "executable": "/System/Applications/Utilities/Terminal.app/Contents/macOS/Terminal",
        "followTheme": true,
        "name": "",
        "platforms": {
          "darwin": true
        },
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "external"
      },
      "darwinIntegratedDefault": {
        "args": [
          "--login"
        ],
        "environment": [],
        "executable": "/bin/zsh",
        "followTheme": true,
        "name": "",
        "platforms": {
          "darwin": true
        },
        "pythonExecutable": "python3",
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "integrated",
        "win32Backend": "conpty"
      },
      "developerConsole": {
        "followTheme": true,
        "name": "",
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "developerConsole"
      },
      "linuxExternalDefault": {
        "args": [],
        "environment": [],
        "executable": "xterm",
        "followTheme": true,
        "name": "",
        "platforms": {
          "linux": true
        },
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "external"
      },
      "linuxIntegratedDefault": {
        "args": [],
        "environment": [],
        "executable": "/bin/sh",
        "followTheme": true,
        "name": "",
        "platforms": {
          "linux": true
        },
        "pythonExecutable": "python3",
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "integrated",
        "win32Backend": "conpty"
      },
      "win32ExternalDefault": {
        "args": [],
        "environment": [],
        "executable": "C:\\Windows\\System32\\cmd.exe",
        "followTheme": true,
        "name": "",
        "platforms": {
          "win32": true
        },
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "external"
      },
      "win32IntegratedDefault": {
        "args": [],
        "environment": [],
        "executable": "C:\\Windows\\System32\\cmd.exe",
        "followTheme": true,
        "name": "",
        "platforms": {
          "win32": true
        },
        "pythonExecutable": "",
        "restoreHistory": false,
        "rightClickAction": "copyPaste",
        "successExitCodes": [
          "0",
          "SIGINT",
          "SIGTERM"
        ],
        "terminalOptions": {
          "documentOverride": null
        },
        "type": "integrated",
        "win32Backend": "conpty"
      }
    },
    "defaultProfile": "darwinIntegratedDefault",
    "terminalOptions": {
      "documentOverride": null
    }
  },
  "obsidian-git": {
    "commitMessage": "vault backup: {{date}}",
    "autoCommitMessage": "vault backup: {{date}}",
    "commitMessageScript": "",
    "commitDateFormat": "YYYY-MM-DD HH:mm:ss",
    "autoSaveInterval": 10,
    "autoPushInterval": 60,
    "autoPullInterval": 60,
    "autoPullOnBoot": true,
    "autoCommitOnlyStaged": false,
    "disablePush": false,
    "pullBeforePush": true,
    "squashCommitsBeforePush": false,
    "disablePopups": false,
    "showErrorNotices": true,
    "disablePopupsForNoChanges": false,
    "listChangedFilesInMessageBody": false,
    "showStatusBar": true,
    "updateSubmodules": false,
    "syncMethod": "merge",
    "mergeStrategy": "none",
    "customMessageOnAutoBackup": false,
    "autoBackupAfterFileChange": true,
    "treeStructure": false,
    "refreshSourceControl": true,
    "basePath": "",
    "differentIntervalCommitAndPush": true,
    "changedFilesInStatusBar": false,
    "showedMobileNotice": true,
    "refreshSourceControlTimer": 7000,
    "showBranchStatusBar": true,
    "setLastSaveToLastCommit": false,
    "submoduleRecurseCheckout": false,
    "gitDir": "",
    "showFileMenu": true,
    "authorInHistoryView": "hide",
    "dateInHistoryView": false,
    "diffStyle": "split",
    "hunks": {
      "showSigns": false,
      "hunkCommands": false,
      "statusBar": "disabled"
    },
    "lineAuthor": {
      "show": false,
      "followMovement": "inactive",
      "authorDisplay": "initials",
      "showCommitHash": false,
      "dateTimeFormatOptions": "date",
      "dateTimeFormatCustomString": "YYYY-MM-DD HH:mm",
      "dateTimeTimezone": "viewer-local",
      "coloringMaxAge": "1y",
      "colorNew": {
        "r": 255,
        "g": 150,
        "b": 150
      },
      "colorOld": {
        "r": 120,
        "g": 160,
        "b": 255
      },
      "textColorCss": "var(--text-muted)",
      "ignoreWhitespace": false,
      "lastShownAuthorDisplay": "initials",
      "lastShownDateTimeFormatOptions": "date"
    }
  },
  "superier-highlighter": {
    "toolbarPosition": "text",
    "defaultHighlightColor": "",
    "enableHaptics": true,
    "showRemoveButton": true,
    "enableColorPalette": true,
    "showOnlyAssignedColors": true,
    "semanticColors": [
      {
        "color": "red",
        "meaning": ""
      },
      {
        "color": "orange",
        "meaning": ""
      },
      {
        "color": "yellow",
        "meaning": ""
      },
      {
        "color": "green",
        "meaning": ""
      },
      {
        "color": "blue",
        "meaning": ""
      },
      {
        "color": "purple",
        "meaning": ""
      }
    ],
    "showNavigatorButton": true,
    "showTooltips": false,
    "enableSmartParagraphSelection": false,
    "learnedNormRules": []
  }
}''')
PLUGINS = {
    "terminal": "polyipseity/obsidian-terminal",
    "obsidian-git": "Vinzent03/obsidian-git",
    "superier-highlighter": "owjxyz/Obsidian-Superier-Highlighter",
}
PLUGIN_HOTKEYS = {
    "terminal": {
        "terminal:find-in-terminal": [{"modifiers": ["Alt"], "key": "F"}],
        "terminal:close-terminal": [{"modifiers": ["Alt"], "key": "W"}],
        "terminal:open-terminal.integrated.root": [
            {"key": "H", "modifiers": ["Mod", "Shift"]},
            {"modifiers": ["Alt"], "key": "T"},
        ],
    },
    "superier-highlighter": {
        **{f"superier-highlighter:apply-color-{index}": [{"modifiers": ["Alt"], "key": key}]
           for index, key in enumerate("ADSZCX", 1)},
        "superier-highlighter:remove-highlight": [{"modifiers": ["Alt"], "key": "Q"}],
    },
}
LEGACY_HIGHLIGHTS = {"editor:toggle-highlight"} | {
    f"editor:toggle-highlight-{color}"
    for color in ["red", "orange", "yellow", "green", "blue", "purple"]
}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Obsidian-Vault-Init"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
    if not content:
        raise ValueError(f"Empty download: {url}")
    return content


def merge_hotkeys(raw, preset, replace_conflicts):
    # Reuse Basic Color Highlighter's validation and merge rules.
    current = json.loads(raw)
    if not isinstance(current, dict):
        raise ValueError("hotkeys.json must contain a JSON object.")
    for command, bindings in current.items():
        if not isinstance(bindings, list):
            raise ValueError(f"Invalid hotkeys for {command}.")
        for binding in bindings:
            if (not isinstance(binding, dict)
                    or not isinstance(binding.get("key"), str) or not binding["key"]
                    or not isinstance(binding.get("modifiers"), list)
                    or any(not isinstance(mod, str) or mod not in {"Mod", "Ctrl", "Meta", "Alt", "Shift"}
                           for mod in binding["modifiers"])):
                raise ValueError(f"Invalid key combination for {command}.")
    if "superier-highlighter:remove-highlight" in preset:
        current = {command: bindings for command, bindings in current.items()
                   if not command.startswith("reader-highlighter-tags:") and command not in LEGACY_HIGHLIGHTS}

    def combination(binding):
        modifiers = {("Meta" if sys.platform == "darwin" else "Ctrl") if mod == "Mod" else mod
                     for mod in binding["modifiers"]}
        return frozenset(modifiers), binding["key"].upper()

    reserved = {combination(binding) for bindings in preset.values() for binding in bindings}
    merged = dict(current)
    for command, bindings in current.items():
        if command in preset:
            continue
        remaining = [binding for binding in bindings
                     if combination(binding) not in reserved]
        if len(remaining) != len(bindings):
            if not replace_conflicts:
                raise ValueError(f"Hotkey conflict: {command}. Use --replace-conflicts to reassign it.")
            merged[command] = remaining
    merged.update(preset)
    return json_bytes(merged)


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def install(vault, only="all", replace_conflicts=False):
    config = vault.expanduser().resolve() / ".obsidian"
    if not config.is_dir():
        raise ValueError("Choose an existing vault containing .obsidian.")
    config = config.resolve()
    if only not in {"all", "terminal", "git", "reader", "highlighter", "shortcuts"}:
        raise ValueError("Choose all, terminal, git, highlighter or shortcuts.")
    selected = (list(PLUGINS) if only == "all" else [] if only == "shortcuts" else
                [{"terminal": "terminal", "git": "obsidian-git",
                  "reader": "superier-highlighter", "highlighter": "superier-highlighter"}[only]])
    enabled_path = config / "community-plugins.json"
    enabled = json.loads(enabled_path.read_bytes()) if enabled_path.exists() else []
    if not isinstance(enabled, list) or any(not isinstance(item, str) for item in enabled):
        raise ValueError("community-plugins.json must contain a list of plugin IDs.")
    updates = {}
    preset = {}
    for plugin in (PLUGINS if only == "shortcuts" else selected):
        preset.update(PLUGIN_HOTKEYS.get(plugin, {}))
    if preset:
        hotkeys = config / "hotkeys.json"
        updates[hotkeys] = merge_hotkeys(hotkeys.read_bytes() if hotkeys.exists() else b"{}", preset, replace_conflicts)
    # Finish every download and validate every manifest before writing anything.
    for plugin in selected:
        repo = PLUGINS[plugin]
        release = json.loads(download(f"https://api.github.com/repos/{repo}/releases/latest"))
        tag = release.get("tag_name")
        if not isinstance(tag, str) or not tag or release.get("draft") or release.get("prerelease"):
            raise ValueError(f"No stable release is available for {plugin}.")
        version = tag.removeprefix("v")
        assets = {asset["name"]: asset for asset in release.get("assets", [])}
        if not {"manifest.json", "main.js", "styles.css"}.issubset(assets):
            raise ValueError(f"The latest release is missing required files for {plugin}.")
        base = f"https://github.com/{repo}/releases/download/{quote(tag, safe='')}/"
        def verified_download(name):
            content = download(base + name)
            digest = assets[name].get("digest")
            if digest and digest != "sha256:" + hashlib.sha256(content).hexdigest():
                raise ValueError(f"Checksum mismatch: {plugin}/{name}.")
            return content
        manifest = verified_download("manifest.json")
        metadata = json.loads(manifest)
        if not isinstance(metadata, dict) or metadata.get("id") != plugin or metadata.get("version") != version:
            raise ValueError(f"Unexpected release manifest for {plugin}.")
        directory = config / "plugins" / plugin
        updates[directory / "manifest.json"] = manifest
        for name in ["main.js", "styles.css"]:
            updates[directory / name] = verified_download(name)
        updates[directory / "data.json"] = json_bytes(SETTINGS[plugin])
        if plugin not in enabled:
            enabled.append(plugin)
    # Enable plugins only after their files and settings have been written.
    if selected:
        if "superier-highlighter" in selected:
            enabled = [plugin for plugin in enabled if plugin != "reader-highlighter-tags"]
        updates[enabled_path] = json_bytes(enabled)
    before = {}
    for path in updates:
        path.resolve().relative_to(config)
        if path.is_symlink():
            raise ValueError(f"Refusing to replace a symlink: {path}")
        before[path] = path.read_bytes() if path.exists() else None
    changes = {path: content for path, content in updates.items() if content != before[path]}
    if not changes:
        print("Already applied; no files changed.")
        return None
    backup = config / "vault-setup-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup.resolve().relative_to(config)
    backup.mkdir(parents=True)
    for path in changes:
        if before[path] is not None:
            saved = backup / path.relative_to(config)
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(before[path])
    (backup / "created-files.json").write_bytes(json_bytes(
        [str(path.relative_to(config)) for path in changes if before[path] is None]))
    print(f"Backup: {backup}")
    written = []
    try:
        # ponytail: offline installer; close Obsidian. Live changes need in-app coordination.
        for path, content in changes.items():
            if (path.read_bytes() if path.exists() else None) != before[path]:
                raise ValueError(f"Settings changed during install: {path}. Close Obsidian and retry.")
            atomic_write(path, content)
            written.append(path)
    except Exception:
        for path in reversed(written):
            if before[path] is None:
                path.unlink()
            else:
                atomic_write(path, before[path])
        raise
    print(f"Applied {only} setup to {config.parent}. Reopen Obsidian.")
    return backup


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", nargs="?", type=Path, default=Path.cwd(), help="Vault root; defaults to current directory.")
    parser.add_argument("--only", choices=["all", "terminal", "git", "reader", "highlighter", "shortcuts"], default="all")
    parser.add_argument("--replace-conflicts", action="store_true", help="Reassign conflicting custom shortcuts.")
    args = parser.parse_args()
    try:
        install(args.vault, args.only, args.replace_conflicts)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
