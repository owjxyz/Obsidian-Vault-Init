# Obsidian Vault Init

One-line installers for saved Terminal, Git, Reader Highlighter Tags and shortcut settings.

macOS · Obsidian 1.14+ · Python 3.9+ · Git

**Quit Obsidian and run from your vault folder. Reopen Obsidian afterward.** Allow community plugins if prompted.

[KOREAN](README.ko.md)

## Install all

Terminal + Git + Reader Highlighter Tags + all saved shortcuts:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 -
```

## Terminal

[Terminal 3.29.0](https://github.com/polyipseity/obsidian-terminal) with the saved settings and macOS integrated zsh profile.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only terminal
```

Shortcuts: **Option + T** or **Cmd + Shift + H** to open, **Option + F** to find, **Option + W** to close.

## Git

[Git 2.42.0](https://github.com/Vinzent03/obsidian-git) with the saved automatic commit-and-sync settings. Git, your vault's repository, remote and authentication must already be configured.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only git
```

## Reader Highlighter Tags

[Reader Highlighter Tags 2.0.0](https://github.com/DuckTapeKiller/obsidian-reader-highlighter-tags), using the current default settings.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only reader
```

Reading view shortcuts: **Ctrl + 1** red, **Ctrl + Q** yellow, **Ctrl + A** green, **Ctrl + Z** purple.

## Highlight shortcuts

The original [Basic Color Highlighter](https://github.com/owjxyz/Basic-Color-Highlighter) command:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Basic-Color-Highlighter/main/apply.py | python3 -
```

| Color | macOS | Windows / Linux | Markdown |
| --- | --- | --- | --- |
| Red | Option + 1 | Alt + 1 | `==🔴text==` |
| Orange | Option + 2 | Alt + 2 | `==🟠text==` |
| Yellow | Option + Q | Alt + Q | `==🟡text==` |
| Green | Option + A | Alt + A | `==🟢text==` |
| Blue | Option + S | Alt + S | `==🔵text==` |
| Purple | Option + Z | Alt + Z | `==🟣text==` |

Select text and press the shortcut.

## Options

- **Another vault:** append `"/path/to/vault"` after `python3 -`.
- **Shortcut conflicts:** append `--replace-conflicts` to reassign conflicting custom shortcuts.
- **Backup:** replaced files are saved under `.obsidian/vault-setup-backups/`. The original highlight-only command uses `.obsidian/hotkeys.json.*.bak`.

Plugin installers download the listed versions from their official releases, replace the selected plugins' settings and add them to the enabled plugin list. Other plugins and notes are preserved. The default target is the current folder, which must contain `.obsidian`.
