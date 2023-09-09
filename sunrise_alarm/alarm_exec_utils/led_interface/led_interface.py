"""Define an interface for controlling LEDs."""
from abc import ABC, abstractmethod


class LEDInterface(ABC):
    """An abstract base class for LED interfaces."""

    @abstractmethod
    def connect(self) -> None:
        """
        Connect to the LEDs, if required by the specific LED implementation.

        Raises:
            RuntimeError: If the LEDs cannot be connected to.
        """
        pass

    @abstractmethod
    def set(self, rgb: tuple[int], intensity: float) -> None:
        """
        Set the desired RGB color and intensity on the LEDs.

        Args:
            rgb: A tuple of integer RGB color values [0, 255] to display.
            intensity: A float representing the intensity or brightness of the LEDs.
                Values less than 0 or greater than 1 will clamp to 0 or 1, respectively.
        """
        pass

    def clamp_intensity(self, intensity: float) -> float:
        """
        Clamp the intensity value to the range [0, 1].

        Args:
            intensity: A float representing the intensity or brightness of the LEDs.

        Returns:
            A float representing the intensity or brightness of the LEDs, clamped to [0, 1].
        """
        return max(0, min(intensity, 1))

    def clamp_rgb(self, rgb: tuple[int]) -> tuple[int]:
        """
        Clamp the RGB values to the range [0, 255].

        Args:
            rgb: A tuple of integer RGB color values [0, 255] to display.

        Returns:
            A tuple of integer RGB color values [0, 255] to display, clamped to [0, 255].
        """
        return [max(0, min(color, 255)) for color in rgb]
