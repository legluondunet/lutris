from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from lutris.exceptions import GameConfigError
from lutris.runners.flatpak import flatpak


class TestFlatpakGameDirectory(TestCase):
    def runner(self, directory="", **options):
        runner = object.__new__(flatpak)
        runner._config = SimpleNamespace(game_config={"appid": "technology.haniwa.ai5-sdl2", **options})
        runner.game_data = {"directory": directory}
        return runner

    def command(self, runner):
        with patch("lutris.util.flatpak.get_command", return_value=["flatpak"]):
            return runner.play()["command"]

    def test_external_data_and_quoted_font(self):
        command = self.command(self.runner("/home/test/Games/YU NO", args='--font "MS PGothic.ttf"'))
        self.assertEqual(
            command,
            [
                "flatpak",
                "run",
                "--user",
                "--filesystem=/home/test/Games/YU NO:rw",
                "--cwd=/home/test/Games/YU NO",
                "technology.haniwa.ai5-sdl2",
                "--font",
                "MS PGothic.ttf",
            ],
        )

    def test_relative_working_directory(self):
        command = self.command(self.runner("/home/test/Games/yuno", working_dir="data"))
        self.assertIn("--cwd=/home/test/Games/yuno/data", command)
        self.assertIn("--filesystem=/home/test/Games/yuno:rw", command)
        self.assertIn("--filesystem=/home/test/Games/yuno/data:rw", command)

    def test_imported_application_has_no_automatic_grant(self):
        command = self.command(self.runner(install_type="system"))
        self.assertEqual(command, ["flatpak", "run", "--system", "technology.haniwa.ai5-sdl2"])

    def test_host_spawn_preserves_data_arguments(self):
        with patch("lutris.util.flatpak.get_command", return_value=["flatpak-spawn", "--host", "flatpak"]):
            command = self.runner("/home/test/Games/yuno").play()["command"]
        self.assertEqual(command[:4], ["flatpak-spawn", "--host", "flatpak", "run"])
        self.assertIn("--cwd=/home/test/Games/yuno", command)

    def test_never_exposes_root_or_interprets_permission_suffixes(self):
        for directory in ("/", "/home/test/Games/yuno:ro"):
            with self.subTest(directory=directory), self.assertRaises(GameConfigError):
                self.command(self.runner(directory))
