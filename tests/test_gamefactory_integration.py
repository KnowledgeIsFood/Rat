from __future__ import annotations

import unittest

from tools import gamefactory_env as gf


class GameFactoryIntegrationTest(unittest.TestCase):
    def test_task_packet_pins_godot_and_existing_project(self) -> None:
        packet = gf.load_task_packet()

        self.assertEqual("rat.gamefactory.task_packet.v1", packet["schema"])
        self.assertEqual("godot", packet["engine"])
        self.assertEqual("godot", packet["engine_identifier"])
        self.assertEqual("4.6.0", packet["engine_version"])
        self.assertEqual("gameR_wucang_shanjing_godot", packet["game_id"])
        self.assertEqual("game", packet["godot_project"])
        self.assertEqual(
            "third_party/GameFactory-3A/agent_skills/setting_overview.md",
            packet["framework"]["entry_skill"],
        )
        self.assertTrue((gf.WORKSPACE_ROOT / packet["godot_project"] / "project.godot").is_file())
        self.assertTrue((gf.WORKSPACE_ROOT / packet["canon"]["master_csv"]).is_file())

    def test_framework_entry_files_exist(self) -> None:
        self.assertEqual([], gf.missing_framework_files())
        self.assertTrue(gf.SETTING_OVERVIEW.is_file())
        overview = gf.SETTING_OVERVIEW.read_text(encoding="utf-8")
        self.assertIn("End-to-end game-generation workflow", overview)
        self.assertIn("godot_api.md", overview)

    def test_godot_client_reports_rat_project_without_engine_probe(self) -> None:
        info = gf.adapter_info(probe_version=False)

        self.assertTrue(info.get("ok"), info)
        payload = info["payload"]
        self.assertEqual("v1", payload["api_version"])
        self.assertEqual("Rat", payload["project_name"])
        self.assertEqual(str(gf.GODOT_PROJECT), payload["project_path"])
        self.assertTrue(payload["project_exists"])
        self.assertEqual("res://main.tscn", payload["main_scene"])
        self.assertEqual(str(gf.GAMEFACTORY_ROOT), payload["gamefactory_root"])

    def test_export_env_points_pythonpath_at_framework(self) -> None:
        script = gf.export_env_shell()

        self.assertIn(str(gf.GAMEFACTORY_ROOT), script)
        self.assertIn(str(gf.GODOT_PROJECT), script)
        self.assertIn("gameR_wucang_shanjing_godot", script)
        self.assertIn("A3GAME_GODOT_PROJECT", script)


if __name__ == "__main__":
    unittest.main()
