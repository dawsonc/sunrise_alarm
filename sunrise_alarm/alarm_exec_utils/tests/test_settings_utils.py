"""Test the sunrise alarm settings utilities."""
import unittest
import os
import shutil
import tempfile
from datetime import time

from ..settings_utils import load_settings, check_disabled, Settings


class TestSettingsUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory and set it as the current working directory
        self.test_dir = tempfile.mkdtemp()

        # Create a temporary "alarm_settings.txt" file for testing
        with open(
            os.path.join(self.test_dir, "alarm_settings.txt"), "w"
        ) as settings_file:
            settings_file.write("07:30     # alarm start time\n")
            settings_file.write("08:00     # alarm maximum brightness time\n")
            settings_file.write(
                "0.75      # fraction of maximum LED power at max brightness\n"
            )
            settings_file.write("255 0 0   # color of alarm\n")

    def tearDown(self):
        # Remove the temporary test directory and its contents after testing
        shutil.rmtree(self.test_dir)

    def test_load_settings(self):
        # Test loading valid settings
        expected_settings = Settings(
            start_time=time(7, 30),
            max_brightness_time=time(8, 0),
            intensity=0.75,
            color=(255, 0, 0),
        )
        loaded_settings = load_settings(self.test_dir)
        print(loaded_settings)
        print(expected_settings)
        self.assertEqual(loaded_settings, expected_settings)

        # Test loading settings with invalid intensity (clipped to [0, 1])
        with open(
            os.path.join(self.test_dir, "alarm_settings.txt"), "w"
        ) as settings_file:
            settings_file.write("07:30\n08:00\n1.5\n255 0 0")

        expected_settings = Settings(
            start_time=time(7, 30),
            max_brightness_time=time(8, 0),
            intensity=1.0,  # Clipped to 1.0
            color=(255, 0, 0),
        )
        loaded_settings = load_settings(self.test_dir)
        self.assertEqual(loaded_settings, expected_settings)

        # Test loading settings with missing file (should raise FileNotFoundError)
        os.remove(os.path.join(self.test_dir, "alarm_settings.txt"))
        with self.assertRaises(FileNotFoundError):
            load_settings(self.test_dir)

    def test_check_disabled(self):
        # Test when "disable_alarm" file is present
        with open(os.path.join(self.test_dir, "disable_alarm"), "w") as _:
            pass

        self.assertTrue(check_disabled(self.test_dir))
        os.remove(os.path.join(self.test_dir, "disable_alarm"))

        # Test when "disable_alarm" file is not present
        self.assertFalse(check_disabled(self.test_dir))


if __name__ == "__main__":
    unittest.main()
