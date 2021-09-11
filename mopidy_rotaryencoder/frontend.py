import pykka
import traceback
from mopidy import core


class RotaryEncoderFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RotaryEncoderFrontend, self).__init__()
        self.core = core

        self.volume_delta = config['rotaryencoder']['volume_delta']
        self._old_volume = 10

        from .gpio_input_manager import GPIOManager
        self.gpio_manager = GPIOManager(self, config['rotaryencoder'])



    def input(self, input_event):
        try:
            if input_event['key'] == 'volume_up':
                current = self.core.mixer.get_volume().get()
                current += self.volume_delta
                if current > 100:
                    current = 100
                self.core.mixer.set_volume(current)
            elif input_event['key'] == 'volume_down':
                current = self.core.mixer.get_volume().get()
                current -= self.volume_delta
                if current < 0:
                    current = 0
                self.core.mixer.set_volume(current)
            elif input_event['key'] == 'mute':
                volume = self.core.mixer.get_volume().get()
                if volume == 0:
                    self.core.mixer.set_volume(self._old_volume)
                else:
                    self._old_volume = volume
                    self.core.mixer.set_volume(0)

        except Exception:
            traceback.print_exc()
