"""Resolve 3AGameFactory paths and environment for the Rat workspace."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
GAMEFACTORY_ROOT = WORKSPACE_ROOT / "third_party" / "GameFactory-3A"
GODOT_PROJECT = WORKSPACE_ROOT / "game"
TASK_PACKET_PATH = WORKSPACE_ROOT / "docs" / "gamefactory" / "task_packet.json"
SETTING_OVERVIEW = (
    GAMEFACTORY_ROOT / "agent_skills" / "setting_overview.md"
)
GODOT_API = (
    GAMEFACTORY_ROOT / "agent_skills" / "engine_context" / "godot_api.md"
)
GODOT_INSTALLER = (
    GAMEFACTORY_ROOT / "scripts" / "engine_install" / "godot" / "install.sh"
)
DEFAULT_GODOT_VERSION = "4.6.0"
DEFAULT_GODOT_EXECUTABLE = WORKSPACE_ROOT / ".tools" / "bin" / "godot4"
REQUIRED_FRAMEWORK_FILES = (
    SETTING_OVERVIEW,
    GODOT_API,
    GAMEFACTORY_ROOT / "engine_adapters" / "godot" / "godot_client.py",
    GAMEFACTORY_ROOT / "pipeline" / "common" / "paths.py",
    GODOT_INSTALLER,
)


def load_task_packet() -> dict[str, Any]:
    payload = json.loads(TASK_PACKET_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("task packet must be a JSON object")
    return payload


def resolved_godot_executable() -> Path | None:
    for candidate in (
        os.environ.get("A3GAME_GODOT_EXECUTABLE", "").strip(),
        os.environ.get("A3GAME_GODOT", "").strip(),
        str(DEFAULT_GODOT_EXECUTABLE),
    ):
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if path.is_file():
            return path
    return None


def environment_map() -> dict[str, str]:
    env = {
        "A3GAME_GODOT_PROJECT": str(GODOT_PROJECT),
        "PYTHONPATH": str(GAMEFACTORY_ROOT),
        "A3GAMEFACTORY_REPO": str(GAMEFACTORY_ROOT),
        "A3GAME_GAME_ID": load_task_packet()["game_id"],
    }
    executable = resolved_godot_executable()
    if executable is not None:
        env["A3GAME_GODOT_EXECUTABLE"] = str(executable)
    return env


def ensure_pythonpath() -> None:
    root = str(GAMEFACTORY_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def missing_framework_files() -> list[str]:
    return [
        str(path.relative_to(WORKSPACE_ROOT))
        for path in REQUIRED_FRAMEWORK_FILES
        if not path.is_file()
    ]


def adapter_info(*, probe_version: bool = False) -> dict[str, Any]:
    missing = missing_framework_files()
    if missing:
        return {
            "ok": False,
            "operation": "rat.gamefactory.adapter_info",
            "artifacts": [],
            "diagnostics": [],
            "warnings": [],
            "errors": [f"missing framework files: {missing}"],
            "payload": {},
        }
    ensure_pythonpath()
    from engine_adapters.godot import GodotClient

    kwargs: dict[str, Any] = {"project_path": GODOT_PROJECT, "api_version": "v1"}
    executable = resolved_godot_executable()
    if executable is not None:
        kwargs["godot_executable"] = executable
    client = GodotClient(**kwargs)
    info = client.get_environment_info(probe_version=probe_version)
    info.setdefault("payload", {})
    info["payload"]["gamefactory_root"] = str(GAMEFACTORY_ROOT)
    info["payload"]["task_packet"] = str(TASK_PACKET_PATH)
    info["payload"]["setting_overview"] = str(SETTING_OVERVIEW)
    return info


def export_env_shell() -> str:
    lines = [
        f'export PYTHONPATH="{GAMEFACTORY_ROOT}${{PYTHONPATH:+:$PYTHONPATH}}"',
        f'export A3GAMEFACTORY_REPO="{GAMEFACTORY_ROOT}"',
        f'export A3GAME_GODOT_PROJECT="{GODOT_PROJECT}"',
        f'export A3GAME_GAME_ID="{load_task_packet()["game_id"]}"',
        f'cd "{GAMEFACTORY_ROOT}"',
    ]
    executable = resolved_godot_executable()
    if executable is not None:
        lines.insert(3, f'export A3GAME_GODOT_EXECUTABLE="{executable}"')
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rat 3AGameFactory environment helper")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("print-env")
    commands.add_parser("export-env")
    info = commands.add_parser("adapter-info")
    info.add_argument("--probe-version", action="store_true")
    commands.add_parser("check")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "print-env":
        print(json.dumps(environment_map(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "export-env":
        sys.stdout.write(export_env_shell())
        return 0
    if args.command == "check":
        missing = missing_framework_files()
        packet = load_task_packet()
        payload = {
            "ok": not missing,
            "missing": missing,
            "game_id": packet.get("game_id"),
            "engine": packet.get("engine"),
            "godot_project": str(GODOT_PROJECT),
            "gamefactory_root": str(GAMEFACTORY_ROOT),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["ok"] else 1
    result = adapter_info(probe_version=args.probe_version)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
