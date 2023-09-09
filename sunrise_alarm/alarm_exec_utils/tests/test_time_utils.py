"""Test the time_utils module."""
import unittest
from datetime import time

from ..settings_utils import Settings
from ..time_utils import before, interpolate_times, get_desired_intensity


class TestTimeFunctions(unittest.TestCase):
    def test_before(self):
        # Test when current time is before target time
        current_time = time(8, 0, 0)
        target_time = time(12, 0, 0)
        self.assertTrue(before(current_time, target_time))

        # Test when current time is equal to target time
        current_time = time(12, 0, 0)
        target_time = time(12, 0, 0)
        self.assertFalse(before(current_time, target_time))

        # Test when current time is after target time
        current_time = time(16, 0, 0)
        target_time = time(12, 0, 0)
        self.assertFalse(before(current_time, target_time))

    def test_interpolate_times(self):
        # Test when current time is before time1
        current_time = time(8, 0, 0)
        time1 = time(12, 0, 0)
        time2 = time(16, 0, 0)
        self.assertEqual(interpolate_times(current_time, time1, time2), 0.0)

        # Test when current time is after time2
        current_time = time(18, 0, 0)
        time1 = time(12, 0, 0)
        time2 = time(16, 0, 0)
        self.assertEqual(interpolate_times(current_time, time1, time2), 1.0)

        # Test when current time is between time1 and time2
        current_time = time(14, 0, 0)
        time1 = time(12, 0, 0)
        time2 = time(16, 0, 0)
        self.assertEqual(interpolate_times(current_time, time1, time2), 0.5)

        # Test when time1 is after time2 (should raise ValueError)
        current_time = time(14, 0, 0)
        time1 = time(16, 0, 0)
        time2 = time(12, 0, 0)
        with self.assertRaises(ValueError):
            interpolate_times(current_time, time1, time2)

    def test_get_desired_intensity(self):
        # Create a settings object to use
        settings = Settings(
            start_time=time(7, 0, 0),
            max_brightness_time=time(8, 0, 0),
            intensity=0.75,
            color=(255, 0, 0),
        )

        # Test when current time is before start time
        current_time = time(6, 0, 0)
        self.assertEqual(get_desired_intensity(current_time, settings), 0.0)

        # Test when current time is after max brightness time
        current_time = time(9, 0, 0)
        self.assertEqual(get_desired_intensity(current_time, settings), 0.75)

        # Test when current time is between start time and max brightness time
        current_time = time(7, 30, 0)
        self.assertEqual(get_desired_intensity(current_time, settings), 0.375)


if __name__ == "__main__":
    unittest.main()
