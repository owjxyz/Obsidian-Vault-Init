# Obsidian Vault Init

Terminal·Git·Superier Highlighter의 최신 정식 릴리스와 저장된 개인 설정·단축키를 한 줄로 적용합니다.

macOS · Obsidian · Python 3.9 이상 · Git

**Obsidian을 종료하고 대상 vault 폴더에서 실행한 뒤, Obsidian을 다시 여세요.** 커뮤니티 플러그인 허용 안내가 나오면 허용합니다.

[ENGLISH](README.md)

## 설치

Terminal + Git + Superier Highlighter + 저장된 모든 단축키:

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 -
```

플러그인을 설치할 때마다 GitHub의 최신 정식 릴리스를 조회하며 시험 배포는 제외합니다. 스크립트를 실행할 때 업데이트하며 상시 자동 업데이트는 등록하지 않습니다. 모든 파일을 내려받고 배포 정보와 제공되는 GitHub 체크섬을 검증한 뒤 보관함을 변경합니다. 조회나 다운로드에 실패하면 보관함을 변경하지 않습니다.

### Terminal

[Terminal](https://github.com/polyipseity/obsidian-terminal)과 저장된 설정, macOS 내장 zsh 프로필을 적용합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only terminal
```

단축키: 열기 **Option + T** 또는 **Cmd + Shift + H**, 검색 **Option + F**, 닫기 **Option + W**.

### Git

[Git](https://github.com/Vinzent03/obsidian-git)과 저장된 자동 커밋·동기화 설정을 적용합니다. Git 설치, vault의 Git 저장소·원격 주소·인증은 미리 설정되어 있어야 합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only git
```

### Superier Highlighter

[Superier Highlighter](https://github.com/owjxyz/Obsidian-Superier-Highlighter)에 저장된 설정과 편집·읽기 공통 단축키를 적용합니다. 툴바는 텍스트 옆에 표시하고, 6색 팔레트와 내비게이터는 활성화하며, 툴팁과 스마트 문단 선택은 비활성화합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only highlighter
```

### 개인 단축키만 적용

플러그인을 다운로드하거나 활성화하지 않고 Terminal을 포함한 모든 개인 단축키를 적용합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/owjxyz/Obsidian-Vault-Init/main/install.py | python3 - --only shortcuts
```

| 색상 / 동작 | 편집·읽기 공통 |
| --- | --- |
| 빨강 | Option + A |
| 주황 | Option + D |
| 노랑 | Option + S |
| 초록 | Option + Z |
| 파랑 | Option + C |
| 보라 | Option + X |
| 하이라이트 제거 | Option + Q |

Windows / Linux에서는 Option 대신 Alt를 사용합니다. 편집·읽기 보기 모두 Superier Highlighter에서 처리합니다. 색상 단축키를 다시 누르면 선택 범위를 포함하는 하이라이트와 색상 표시를 제거합니다.

## 옵션

- **다른 vault:** `python3 -` 뒤에 `"/대상/vault/경로"`를 추가합니다.
- **단축키 충돌:** `--replace-conflicts`를 추가하면 충돌하는 기존 사용자 지정 키 배정을 해제합니다.
- **백업:** 교체되는 파일은 `.obsidian/vault-setup-backups/`에 저장합니다.
- **하이라이터 설정:** Reader Highlighter Tags를 비활성화하고 해당 단축키와 `editor:toggle-highlight` 기본·색상별 단축키를 제거합니다.

플러그인을 설치하면 선택한 플러그인의 저장된 설정을 교체하고 활성화 목록에 추가합니다. 노트와 그 외 플러그인의 설정은 보존합니다. 단축키만 적용하면 플러그인 파일과 활성화 상태를 보존합니다. 경로를 생략하면 현재 폴더에 적용하며, `.obsidian` 폴더가 있어야 합니다.
