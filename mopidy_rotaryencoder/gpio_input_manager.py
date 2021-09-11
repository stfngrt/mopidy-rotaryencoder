import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)

class GPIOManager():
    def __init__(self, frontend, pins):

        self.frontend = frontend


        self._current_data = 0
        self._current_clk = 0

        self.correctlyLoaded = False
        self.data_pin = pins['datapin']
        self.clk_pin = pins['clkpin']
        self.sw_pin = pins['swpin']

        try:
            # GPIO Mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.data_pin, GPIO.IN)
            GPIO.setup(self.clk_pin, GPIO.IN)
            GPIO.setup(self.sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.add_event_detect(self.data_pin, GPIO.RISING,
                                  callback=self.rotary_interrupt)
            GPIO.add_event_detect(self.clk_pin, GPIO.RISING,
                                  callback=self.rotary_interrupt)

            # Mute
            GPIO.setup(self.sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.sw_pin, GPIO.RISING, callback=self.mute,
                                  bouncetime=30)

            self.correctlyLoaded = True

        except RuntimeError:
            logger.error("RotaryEncoder: Not enough permission " +
                         "to use GPIO. GPIO input will not work")

    # Rotarty encoder interrupt:
    # this one is called for both inputs from rotary switch (A and B)
    def rotary_interrupt(self, channel):
        # read both of the switches
        data = GPIO.input(self.data_pin)
        clk = GPIO.input(self.clk_pin)
        # now check if state of data or clk has changed
        # if not that means that bouncing caused it
        if self._current_data == data and self._current_clk == clk:  # Same interrupt as before (Bouncing)?
            return  # ignore interrupt!

        self._current_data = data  # remember new state
        self._current_clk = clk  # for next bouncing check

        if data and clk:  # Both one active? Yes -> end of sequence
            if channel == self.clk_pin:  # Turning direction depends on
                self.vol_down()  # increase or decrease counter
            else:  # so depending on direction either
                self.vol_up()  # which input gave last interrupt
        return

    def vol_up(self):
        self.frontend.input({'key': 'volume_up'})

    def vol_down(self):
        self.frontend.input({'key': 'volume_down'})

    def mute(self, channel):
        self.frontend.input({'key': 'mute'})
