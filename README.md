[KOREAN](README.ko.md)

# Obsidian Vault Init

Install the latest stable Terminal, Git and Superier Highlighter releases with saved personal settings and shortcuts.

macOS · Obsidian · Python 3.9+ · Git

**Quit Obsidian and run from your vault folder. Reopen Obsidian afterward.** Allow community plugins if prompted.

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

[Superier Highlighter](https://github.com/owjxyz/Obsidian-Superier-Highlighter) with default plugin settings and the saved reading and editing shortcuts below. This replaces Reader Highlighter Tags in the enabled plugin list and removes its obsolete shortcut bindings; its files remain intact. The older `--only reader` option is an alias for this setup.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only highlighter
```

### Personal shortcuts only

Apply all saved shortcuts, including Terminal, without downloading or enabling plugins:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only shortcuts
```

| Colour / action                   | Editing    | Reading (Superier Highlighter) |
| --------------------------------- | ---------- | ------------------------------ |
| Red                               | Option + A | Ctrl + A                       |
| Orange                            | Option + D | Ctrl + D                       |
| Yellow                            | Option + S | Ctrl + S                       |
| Green                             | Option + Z | Ctrl + Z                       |
| Blue                              | Option + C | Ctrl + C                       |
| Purple                            | Option + X | Ctrl + X                       |
| Toggle default / remove highlight | Option + Q | Ctrl + Q                       |

On Windows / Linux, use Alt instead of Option. The editing colour commands require the existing Basic Color Highlighter customization; this script assigns their shortcuts. Reading shortcuts use Superier Highlighter. Repeating a reading colour shortcut removes the containing highlight and its colour marker.

The standalone Superier Highlighter installer does not configure shortcuts. This repository owns the personal bindings.

## Options

- **Another vault:** append `"/path/to/vault"` after `python3 -`.
- **Shortcut conflicts:** append `--replace-conflicts` to reassign conflicting custom shortcuts.
- **Backup:** replaced files are saved under `.obsidian/vault-setup-backups/`.

Plugin installation replaces the selected plugins' saved settings and enables them. Other plugins and notes are preserved, apart from the legacy highlighter migration described above. Shortcut-only setup preserves plugin files and activation. The default target is the current folder, which must contain `.obsidian`.
