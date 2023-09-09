"""An interface to the Fadecandy LED driver."""
from .led_interface import LEDInterface
from .opc import OPCClient


class FadecandyInterface(LEDInterface):
    """An interface to the Fadecandy LED driver using OpenPixelControl"""

    def __init__(self, address: str = "localhost:7890", num_leds: int = 64):
        """
        Initialize the FadecandyInterface.

        Args:
            address: The address of the Fadecandy server.
            num_leds: The number of LEDs connected to the Fadecandy server.
        """
        self.address = address
        self.num_leds = num_leds

        self.client = None

    def connect(self) -> None:
        """
        Connect to the LEDs, if required by the specific LED implementation.

        Raises:
            RuntimeError: If the LEDs cannot be connected to.
        """
        self.client = OPCClient(self.address)

        if not self.client.can_connect():
            raise RuntimeError(
                f"Could not connect to Fadecandy server at {self.address}"
            )

    def set(self, rgb: tuple[int], intensity: float) -> None:
        """
        Set the desired RGB color and intensity on the LEDs.

        Args:
            rgb: A tuple of integer RGB color values [0, 255] to display.
            intensity: A float representing the intensity or brightness of the LEDs.
                Values less than 0 or greater than 1 will clamp to 0 or 1, respectively.
        """
        # Clamp intensity and color inputs
        intensity = self.clamp_intensity(intensity)
        rgb = self.clamp_rgb(rgb)

        # There is an annoying flicker on Fadecandy below 0.15 intensity, so clamp it
        if 0 < intensity < 0.15:
            intensity = 0.15

        # Scale color by intensity
        rgb = [int(color * intensity) for color in rgb]

        # Set the pixels
        for _ in range(2):  # Do this twice, since otherwise there is lag
            self.client.put_pixels([rgb] * self.num_leds, channel=0)
