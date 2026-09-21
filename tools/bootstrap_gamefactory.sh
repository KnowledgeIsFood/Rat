#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GAMEFACTORY_ROOT="$ROOT/third_party/GameFactory-3A"
GODOT_PROJECT="$ROOT/game"
GODOT_VERSION="${A3GAME_GODOT_VERSION:-4.6.0}"
WITH_GODOT=0
INSTALL_FRAMEWORK=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: bash tools/bootstrap_gamefactory.sh [--with-godot] [--install-framework] [--dry-run]

  --with-godot         Install or reuse Godot 4.6.0 via 3AGameFactory's installer
  --install-framework  Install A3GamePlayable into game/ through GodotClient
  --dry-run            Resolve / validate without writing Godot or plugin files
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-godot) WITH_GODOT=1 ;;
    --install-framework) INSTALL_FRAMEWORK=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ ! -f "$GAMEFACTORY_ROOT/agent_skills/setting_overview.md" ]]; then
  git -C "$ROOT" submodule update --init --recursive third_party/GameFactory-3A
fi

if [[ ! -f "$GAMEFACTORY_ROOT/agent_skills/setting_overview.md" ]]; then
  echo "3AGameFactory is missing at $GAMEFACTORY_ROOT" >&2
  exit 1
fi

export PYTHONPATH="$GAMEFACTORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export A3GAMEFACTORY_REPO="$GAMEFACTORY_ROOT"
export A3GAME_GODOT_PROJECT="$GODOT_PROJECT"

python3 "$ROOT/tools/gamefactory_env.py" check

if [[ "$WITH_GODOT" -eq 1 ]]; then
  installer="$GAMEFACTORY_ROOT/scripts/engine_install/godot/install.sh"
  args=(
    --version "$GODOT_VERSION"
    --install-root "$ROOT/.tools/godot"
    --cache-dir "$ROOT/.cache/godot"
    --bin-dir "$ROOT/.tools/bin"
    --config-dir "$ROOT/.tools/config"
    --json
  )
  if [[ "$DRY_RUN" -eq 1 ]]; then
    args+=(--dry-run)
  fi
  mkdir -p "$ROOT/.tools" "$ROOT/.cache"
  echo "Running Godot installer: $installer ${args[*]}"
  "$installer" "${args[@]}" | tee "$ROOT/.tools/godot-install-result.json"
  if python3 - "$ROOT/.tools/godot-install-result.json" <<'PY'
import json, sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if not payload.get("ok"):
    raise SystemExit("Godot installer reported ok=false")
executable = payload.get("executable") or ""
if executable:
    print(executable)
PY
  then
    executable="$(python3 -c 'import json,sys; from pathlib import Path; print(json.loads(Path(sys.argv[1]).read_text()).get("executable",""))' "$ROOT/.tools/godot-install-result.json")"
    if [[ -n "$executable" ]]; then
      export A3GAME_GODOT_EXECUTABLE="$executable"
    fi
  fi
fi

if [[ "$INSTALL_FRAMEWORK" -eq 1 ]]; then
  cmd=(python3 -m engine_adapters.godot --project "$GODOT_PROJECT" install-framework)
  if [[ "$DRY_RUN" -eq 1 ]]; then
    cmd+=(--dry-run)
  fi
  echo "Installing A3GamePlayable via ${cmd[*]}"
  (cd "$GAMEFACTORY_ROOT" && "${cmd[@]}")
fi

python3 "$ROOT/tools/gamefactory_env.py" print-env
echo "Next: read $GAMEFACTORY_ROOT/agent_skills/setting_overview.md"
echo "Then read $ROOT/docs/gamefactory/task_packet.json"
