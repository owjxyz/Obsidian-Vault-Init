# Obsidian Vault Init

현재 사용하는 Terminal·Git·Reader Highlighter Tags 설정과 단축키를 한 줄로 적용합니다.

macOS · Obsidian 1.14 이상 · Python 3.9 이상 · Git

**Obsidian을 종료하고 대상 vault 폴더에서 실행한 뒤, Obsidian을 다시 여세요.** 커뮤니티 플러그인 허용 안내가 나오면 허용합니다.

## Install

Terminal + Git + Reader Highlighter Tags + 저장된 모든 단축키:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 -
```

### Terminal

[Terminal 3.29.0](https://github.com/polyipseity/obsidian-terminal)과 저장된 설정, macOS 내장 zsh 프로필을 적용합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only terminal
```

단축키: 열기 **Option + T** 또는 **Cmd + Shift + H**, 검색 **Option + F**, 닫기 **Option + W**.

### Git

[Git 2.42.0](https://github.com/Vinzent03/obsidian-git)과 저장된 자동 커밋·동기화 설정을 적용합니다. Git 설치, vault의 Git 저장소·원격 주소·인증은 미리 설정되어 있어야 합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only git
```

### Reader Highlighter Tags

[Reader Highlighter Tags 2.0.0](https://github.com/DuckTapeKiller/obsidian-reader-highlighter-tags)과 현재 사용 중인 기본 설정을 적용합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only reader
```

읽기 보기 단축키: 빨강 **Ctrl + 1**, 노랑 **Ctrl + Q**, 초록 **Ctrl + A**, 보라 **Ctrl + Z**.

### 하이라이트 단축키

기존 [Basic Color Highlighter](https://github.com/owjxyz/Basic-Color-Highlighter) 명령입니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Basic-Color-Highlighter/main/apply.py | python3 -
```

| 색상 | macOS | Windows / Linux | 저장되는 형식 |
| --- | --- | --- | --- |
| 빨강 | Option + 1 | Alt + 1 | `==🔴텍스트==` |
| 주황 | Option + 2 | Alt + 2 | `==🟠텍스트==` |
| 노랑 | Option + Q | Alt + Q | `==🟡텍스트==` |
| 초록 | Option + A | Alt + A | `==🟢텍스트==` |
| 파랑 | Option + S | Alt + S | `==🔵텍스트==` |
| 보라 | Option + Z | Alt + Z | `==🟣텍스트==` |

텍스트를 선택하고 해당 단축키를 누릅니다.

## 옵션

- **다른 vault:** `python3 -` 뒤에 `"/대상/vault/경로"`를 추가합니다.
- **단축키 충돌:** `--replace-conflicts`를 추가하면 충돌하는 기존 사용자 지정 키 배정을 해제합니다.
- **백업:** 교체되는 파일은 `.obsidian/vault-setup-backups/`에 저장합니다. 기존 하이라이트 전용 명령의 백업은 `.obsidian/hotkeys.json.*.bak`입니다.

플러그인 설치 명령은 공식 배포본에서 위 버전을 내려받아 선택한 플러그인의 설정을 교체하고 활성화 목록에 추가합니다. 다른 플러그인과 노트는 보존합니다. 경로를 생략하면 현재 폴더에 적용하며, `.obsidian` 폴더가 있어야 합니다.
