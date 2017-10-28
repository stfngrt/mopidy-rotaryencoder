from __future__ import unicode_literals

import pykka
from mopidy import core

volume_delta = 5

class RotaryEncoderFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(RotaryEncoderFrontend, self).__init__()
        self.core = core

        from .gpio_input_manager import GPIOManager
        self.gpio_manager = GPIOManager(self, config['rotaryencoder'])

    def input(self, input_event):
        try:
            if input_event['key'] == 'volume_up':
                current = self.core.playback.volume.get()
                current += volume_delta
                if current > 100:
                    current = 100
                self.core.playback.volume = current
            elif input_event['key'] == 'volume_down':
                current = self.core.playback.volume.get()
                current -= volume_delta
                if current < 0:
                    current = 0
                self.core.playback.volume = current
            elif input_event['key'] == 'mute':
                self.core.playback.volume = 0
        except Exception:
            traceback.print_exc()
