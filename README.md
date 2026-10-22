# Obsidian Vault Init

Install the latest stable Terminal, Git and Superier Highlighter releases with saved personal settings and shortcuts.

macOS · Obsidian · Python 3.9+ · Git

**Quit Obsidian and run from your vault folder. Reopen Obsidian afterward.** Allow community plugins if prompted.

[KOREAN](README.ko.md)

## Install

Terminal + Git + Superier Highlighter + all saved shortcuts:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 -
```

Every plugin install queries GitHub for the latest stable release. Preview releases are excluded. Updates happen when you run the script; it does not install a background updater. All downloads and manifests are checked before any vault files are changed; available GitHub asset checksums are verified. A failed lookup or download leaves the vault unchanged.

### Terminal

[Terminal](https://github.com/polyipseity/obsidian-terminal) with saved settings and the macOS integrated zsh profile.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only terminal
```

Shortcuts: **Option + T** or **Cmd + Shift + H** to open, **Option + F** to find, **Option + W** to close.

### Git

[Git](https://github.com/Vinzent03/obsidian-git) with saved automatic commit-and-sync settings. Git, your vault's repository, remote and authentication must already be configured.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only git
```

### Superier Highlighter

[Superier Highlighter](https://github.com/owjxyz/Obsidian-Superier-Highlighter) with saved settings and shared editing and reading shortcuts. The toolbar appears by the text, the six-colour palette and navigator are enabled, and tooltips and smart paragraph selection are disabled.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only highlighter
```

### Personal shortcuts only

Apply all saved shortcuts, including Terminal, without downloading or enabling plugins:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only shortcuts
```

| Colour / action | Editing and reading |
| --- | --- |
| Red | Option + A |
| Orange | Option + D |
| Yellow | Option + S |
| Green | Option + Z |
| Blue | Option + C |
| Purple | Option + X |
| Remove highlight | Option + Q |

On Windows / Linux, use Alt instead of Option. Superier Highlighter handles both editing and reading. Repeating a colour shortcut removes the containing highlight and its colour marker.

## Options

- **Another vault:** append `"/path/to/vault"` after `python3 -`.
- **Shortcut conflicts:** append `--replace-conflicts` to reassign conflicting custom shortcuts.
- **Backup:** replaced files are saved under `.obsidian/vault-setup-backups/`.
- **Highlighter setup:** disables Reader Highlighter Tags and clears its shortcuts and the default and colour-specific `editor:toggle-highlight` shortcuts.

Plugin installation replaces the selected plugins' saved settings and enables them. Notes and unrelated plugin settings are preserved. Shortcut-only setup preserves plugin files and activation. The default target is the current folder, which must contain `.obsidian`.
