import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)
data_pin = 0
clk_pin = 0
sw_pin = 0

current_data = 0
current_clk = 0


class GPIOManager():
    def __init__(self, frontend, pins):

        self.frontend = frontend

        self.correctlyLoaded = False

        global data_pin
        global clk_pin
        global sw_pin
        data_pin = pins['datapin']
        clk_pin = pins['clkpin']
        sw_pin = pins['swpin']

        try:
            # GPIO Mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(data_pin, GPIO.IN)
            GPIO.setup(clk_pin, GPIO.IN)
            GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.add_event_detect(data_pin, GPIO.RISING,
                                  callback=self.rotary_interrupt)
            GPIO.add_event_detect(clk_pin, GPIO.RISING,
                                  callback=self.rotary_interrupt)

            # Mute
            GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(sw_pin, GPIO.RISING, callback=self.mute,
                                  bouncetime=30)

            self.correctlyLoaded = True

        except RuntimeError:
            logger.error("RotaryEncoder: Not enough permission " +
                         "to use GPIO. GPIO input will not work")

    # Rotarty encoder interrupt:
    # this one is called for both inputs from rotary switch (A and B)
    def rotary_interrupt(self, channel):
        global current_data, current_clk
        # read both of the switches
        data = GPIO.input(data_pin)
        clk = GPIO.input(clk_pin)
        # now check if state of data or clk has changed
        # if not that means that bouncing caused it
        if current_data == data and current_clk == clk:  # Same interrupt as before (Bouncing)?
            return  # ignore interrupt!

        current_data = data  # remember new state
        current_clk = clk  # for next bouncing check

        if data and clk:  # Both one active? Yes -> end of sequence
            if channel == clk_pin:  # Turning direction depends on
                self.vol_up()  # which input gave last interrupt
            else:  # so depending on direction either
                self.vol_down()  # increase or decrease counter
        return

    def vol_up(self):
        self.frontend.input({'key': 'volume_up'})

    def vol_down(self):
        self.frontend.input({'key': 'volume_down'})

    def mute(self, channel):
        self.frontend.input({'key': 'mute'})
